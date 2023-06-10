# Daily Data Pipeline with Apache Airflow

## Overview
This repository contains the source code for an automated data pipeline built with **Apache Airflow**. \
The pipeline performs daily data processing tasks, including file availability check, file download from **Google Drive API**, loading data into **MongoDB**, **Spark** data processing, and loading processed data back into MongoDB. \
The pipeline is designed to run on an interval schedule, ensuring the timely and automated processing of data.

<img width="1660" alt="Screen Shot 2023-06-10 at 08 44 28" src="https://github.com/minhquyetdo/Daily-Task/assets/135207786/69d00f41-b2a7-4800-bbee-6b4856b24ef0">


**Technical features** in this Data Pipeline:
|Features| Description |
|:------|-----------:|
|**DBMS**|MongoDB|
|**ETL Tool**|Bash, Python, Spark|
|**ETL Oscheration**|Apache Airflow|
|**Parallel Processing**|Tasks can be executed concurrently, reducing the overall processing time and improving efficiency|
|**Automation and Schedule**|The pipeline is designed to run automatically on a daily schedule, eliminating the need for manual intervention|
|**Error Resilience**|The pipeline incorporates error handling mechanisms, such as task retries and error notifications, to handle failures and exceptions|
|**Modularity and Flexibility**|New tasks can be added or modified without affecting the overall workflow, providing flexibility and adaptability|
|**Scalability**|The pipeline can handle large volumes of data due to its parallel processing capabilities and distributed computing with Spark|
|**Environment**|Docker-compose|

#### Explode the repository 
|Files| Description |
|:------|-----------:|
|what-how-why.txt|Data pipeline document|
|airflow.cfg|Airflow config with worker, database backend, broker|
|requirements.txt|The required packages for Python venv|
|.dags/daily-task.py|Source DAG code for data pipeline|
|.dags/toolbox/dailycheck.py|Source code for checking if the daily files available|
|.dags/toolbox/sparkprocess.py|Source code for read and processing data|

## Clone the data pipeline

#### Requirements and Setting Apache Spark
1. Install Apache Spark by following the official documentation: [Apache Spark Installation](https://spark.apache.org/docs/latest/index.html).
2. Set up a Spark cluster or standalone mode according to your requirements.
3. Ensure that the Spark cluster has sufficient resources to handle the data size and computational demands of the analysis.

#### Requirements and Setting for MongoDB
To operate the Finance Data Warehouse, ensure you have the following:

1. **MongoDB**: Install [MongoDB Installation](https://docs.mongodb.com/manual/installation/) on your system or use a MongoDB server. The data warehouse was developed using MongoDB and requires a compatible environment.
2. **Database Setup**: Create a new database in MongoDB to host the data warehouse. You can use the MongoDB shell or a graphical interface to create the necessary collections.
3. **Execution Environment**: Set up a MongoDB instance and ensure it is accessible from your Spark environment. This can be achieved through the MongoDB shell, MongoDB Compass, or by using external tools capable of interacting with MongoDB.

#### Requirements and Setting for Apache Airflow
To install the necessary packages and dependencies for running the daily data pipeline, follow the steps below:

1. Install Apache Airflow by following the official documentation: [Apache Airflow Installation Guide](https://airflow.apache.org/docs/apache-airflow/stable/installation/index.html). \
You might install by [Docker Compose Installation Guide](https://docs.docker.com/compose/install/) with my setting in `docker-compose.yml`, this configuration is for local development.

2. Set up the required connections in Apache Airflow: 

   Configure the MongoDB connection in the Airflow configuration file (`airflow.cfg`) by adding the necessary MongoDB connection details.

3. Install the required Python packages for interacting with Google Drive API, MongoDB, and Spark:

   Use the following command to install the required packages:
```
pip install -r requirements.txt
```

4. Set up the necessary credentials for Google Drive API:

   Follow the Google Drive API documentation to create a project, enable the Drive API, and generate the required credentials (OAuth 2.0 client credentials). \
   Download the credentials JSON file and place it in a secure location.

5. Configure the pipeline: 

   Set up the necessary variables and configurations in the Apache Airflow environment to specify the folder paths, MongoDB collection names, Spark job configurations, and any other pipeline-specific settings.

6. Start the data pipeline using Docker Compose:

   Navigate to the root directory of the cloned repository. 

   Run the following command to start the data pipeline using Docker Compose:
     ```
     docker-compose up -d
     ```

7. Access the Apache Airflow UI:

   Open a web browser and visit `http://localhost:8080` to access the Apache Airflow UI. \
   From the UI, you can monitor the status of the data pipeline, view task execution logs, and manage the workflow.

## License

Feel free to contribute, make improvements, or use the code as a reference for your own database management system.
