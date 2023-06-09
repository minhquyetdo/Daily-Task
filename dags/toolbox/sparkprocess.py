
# Import needed libraries to create a spark session.
# Create a spark session which use "local" machine and all CPU core,
# The session open a reader connect to mongodb localhost, "DailyTask" database.

from pyspark.sql import SparkSession
from pyspark import SparkConf
from pyspark.sql import functions as func
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, LongType, DoubleType, ArrayType

myConf = SparkConf() \
    .setMaster('local[*]') \
    .setAppName('ASM2')

spark = SparkSession \
        .builder \
        .config(conf=myConf) \
        .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:10.1.1") \
        .config("spark.mongodb.read.connection.uri", "mongodb://127.0.0.1:27017/") \
        .config("spark.mongodb.read.database", "DailyTask") \
        .getOrCreate()

# Using the reader connection, create dataframes from reading mongodb collections, change the data to appropriate type.

questionsRawDF = spark.read.format("mongodb").option("spark.mongodb.read.collection", "Questions").load()
questionsDF = questionsRawDF \
    .withColumn("CreationDate", func.to_date(func.col("CreationDate"))) \
    .withColumn("ClosedDate", func.to_date(func.col("ClosedDate"))) \
    .withColumn("OwnerUserId", func.col("OwnerUserId").cast("int")) \
    .drop("_id")

answersRawDF = spark.read.format("mongodb").option("spark.mongodb.read.collection", "Answers").load()
answersDF = answersRawDF \
    .withColumn("CreationDate", func.to_date(func.col("CreationDate"))) \
    .withColumn("OwnerUserId", func.col("OwnerUserId").cast("int")) \
    .drop("_id")

# Create only needed dataframe to reduce work load when join

questionsidDF = questionsDF \
    .select("Id")
answersidDF = answersDF \
    .select("ParentId", func.col("Id").alias("CommentId"))

# Setting join parameter: key and join type

joinExpr = questionsidDF.Id == answersidDF.ParentId
joinType = "left"

# Join and filter through conditions to get the results

totalAnswersDF = questionsidDF \
    .join(answersidDF, joinExpr, joinType) \
    .drop(answersidDF.ParentId) \
    .groupBy("Id") \
    .agg(func.count("*").alias("TotalAnswers")) \
    .sort(func.col("TotalAnswers").desc()) \

# Write the dataframe to csv file with header.
totalAnswersDF.write \
    .option("header",True) \
    .csv("./processed_files/total_answers")
