
# Import all needed libraries, this DAG use Bash, Python - Airflow Core Operator,
# Spark, Google Cloud - Airflow Provider Operator: 

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator 
from airflow.providers.google.cloud.transfers.gdrive_to_local import GoogleDriveToLocalOperator
from datetime import datetime
from textwrap import dedent

# Import custom Python callable function to use in Python Operator,
# All the python script store in "toolbox" folder.
from toolbox import dailycheck


# Create the DAG object with continuous tasks
with DAG('ASM2-pipeline',
        start_date=datetime(2022, 1, 1),
        schedule_interval='@daily',
        catchup=False) as dag:

    
    # Execute bash command that print information to the console. 
    Start = BashOperator(
        task_id='Start',
        bash_command="echo 'Initializing daily pipeline' "
    )
    Start.doc_md = dedent(
        """\
    #### Task Documentation
    This dummy task inform the beginning of daily pipeline task.
    """
    )

    # Execute python function "check_files" in "dailycheck" module,
    # the result return name of the next task.
    Branching = BranchPythonOperator(
        task_id='Branching',
        python_callable=dailycheck.check_files,
        op_kwargs= {'path': '/Users/laclac/downloaded_files'}
    )
    Branching.doc_md = dedent(
        """\
    #### Task Documentation
    First step of the DAG, we check all the file in the "downloaded_files" folder,
    If both of the file "Answers.csv" and "Questions.csv" already there, then the daily task has been done, trigger "End" task.
    If we don't have enough file, then do the daily tasks, trigger "ClearFile" task.
    """
    )

    # Execute bash command that clear the destination folder,
    # and give it permission to write, read, execute for doing tasks.
    ClearFile = BashOperator(
        task_id='ClearFile',
        bash_command='rm -rf /Users/laclac/downloaded_files && mkdir -m 777 /Users/laclac/downloaded_files'
    )
    Branching.doc_md = dedent(
        """\
    #### Task Documentation
    First step of the DAG, we check all the file in the "downloaded_files" folder,
    If both of the file "Answers.csv" and "Questions.csv" already there, then the daily task has been done, trigger "End" task.
    If we don't have enough file, then do the daily tasks, trigger "ClearFile" task.
    """
    )

    # Execute a Google provider operator, that use google drive API to download the file,
    # Must setup a gcp connection to Google Cloud to use this operator
    # This operator allow to download any file with the shared drive id 
    GetAnwersFile = GoogleDriveToLocalOperator(
        gcp_conn_id="gcp-airflow1",
        task_id="GetAnwersFile",
        folder_id="",
        file_name="Answers.csv",
        output_file="./downloaded_files/Answers.csv",
        drive_id="0AM7jW-sxwwaUUk9PVA"
        )
    GetAnwersFile.doc_md = dedent(
        """\
    #### Task Documentation
    This task download the "Answers.csv" file from data source which is Google Drive, store data in the "downloaded_files" folder.
    """
    )
    
    # Execute bash command that use "mongoimport" to import the "Answers.csv" file to mongodb
    # The destination is database "DailyTask", collection "Answers"
    # Must deploy a mongodb server host and setup connection from local machine to database's port.
    ImportAnswersMongo = BashOperator(
        task_id='ImportAnswersMongo',
        bash_command='mongoimport --type csv --db DailyTask --collection Answers --headerline --drop --file /Users/laclac/downloaded_files/Answers.csv'
    )
    ImportAnswersMongo.doc_md = dedent(
        """\
    #### Task Documentation
    This task import the new data "Answers.csv" to the "mongodb" database, new data will be store in database "DailyTask", collection "Answers"
        """
    )

    # Execute a Google provider operator, that use google drive API to download the file,
    # Must setup a gcp connection to Google Cloud to use this operator
    # This operator allow to download any file with the shared drive id
    GetQuestionsFile = GoogleDriveToLocalOperator(
        gcp_conn_id="gcp-airflow1",
        task_id="GetQuestionsFile",
        folder_id="",
        file_name="Questions.csv",
        output_file="./downloaded_files/Questions.csv",
        drive_id="0AM7jW-sxwwaUUk9PVA"
        )
    GetQuestionsFile.doc_md = dedent(
        """\
    #### Task Documentation
    This task download the "Questions.csv" file from data source which is Google Drive, store data in the "downloaded_files" folder.
    """
    )

    # Execute bash command that use "mongoimport" to import the "Questions.csv" file to mongodb
    # The destination is database "DailyTask", collection "Questions"
    # Must deploy a mongodb server host and setup connection from local machine to database's port.
    ImportQuestionsMongo = BashOperator(
        task_id='ImportQuestionsMongo',
        bash_command='mongoimport --type csv --db DailyTask --collection Questions --headerline --drop --file /Users/laclac/downloaded_files/Questions.csv'
    )
    ImportQuestionsMongo.doc_md = dedent(
        """\
    #### Task Documentation
    This task import the new data "Questions.csv" to the "mongodb" database, new data will be store in database "DailyTask", collection "Questions"
        """
    )

    # Execute a Sparksubmit Operator that read and process the data in mongodb,
    # final result will be write to ".csv" file and store in local machine.
    # Must setup a airflow - spark connection to deploy this Operator.
    # Must setup a spark - mongodb to deploy spark-submit.
    # The Spark python script store in "toolbox" folder.
    SparkProcess = SparkSubmitOperator(
		application ='/Users/laclac/airflow/dags/toolbox/sparkprocess.py',
		conn_id= 'spark-local', 
		task_id='spark_submit_task',
        spark_binary='spark-submit'
		)
    SparkProcess.doc_md = dedent(
        """\
    #### Task Documentation
    This task use Spark engine to read and process large data from mongodb then write the result into local disk.
    Final result is the total answers of each questions. 
        """
    )
    
    # Execute bash command that use "mongoimport" to import results files to mongodb
    # The destination is database "DailyTask", collection "TotalAnswer"
    # Must deploy a mongodb server host and setup connection from local machine to database's port.
    ImportResultsMongo = BashOperator(
        task_id='ImportResultsMongo',
        bash_command='cd /Users/laclac/processed_files/total_answers && for filename in *; do mongoimport --type csv --db DailyTask --collection TotalAnswer --headerline --drop --file $filename; done'
    )
    ImportResultsMongo.doc_md = dedent(
        """\
    #### Task Documentation
    This task import the result files in "total_answers" folder to the "mongodb" database, new data will be store in database "DailyTask", collection "TotalAnswer"
        """
    )

    # Execute bash command that print information to the console. 
    End = BashOperator(
        trigger_rule='none_failed',
        task_id='End',
        bash_command="echo 'Daily Task completed!'"
    )
    End.doc_md = dedent(
        """\
    #### Task Documentation
    This dummy task inform the end of daily pipeline task.
    """
    )
    dag.doc_md = """
    ### Daily Data-pipeline.
    - This is a basic automate data-pipeline that cover:
    - Using Command-Line to manipulate OS system task.
    - Check job status.
    - Extract multiple files data from source.
    - Import data in to database.
    - Process large data by using parallel computing Spark Engine.
    - Write result to diversity file types.
    - Store reults into database.
    #### For more detail, please check each task instance detail.
    """

    # This pipe show the connection between tasks, alowing tasks to parallel computing and branching in order.

    Start >> Branching
    
    # Check job status then trigger the next task
    Branching >> [ClearFile, End] 
    
    # Parallel computing to improve performance.
    ClearFile >> [GetAnwersFile, GetQuestionsFile]
    
    GetAnwersFile >> ImportAnswersMongo

    GetQuestionsFile >> ImportQuestionsMongo
    
    # After all_success then execute SparkProcess
    [ImportAnswersMongo, ImportQuestionsMongo] >> SparkProcess >> ImportResultsMongo >> End