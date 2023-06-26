import pyspark
import requests
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, VarcharType, TimestampType, DoubleType, BooleanType
from pyspark.sql.functions import lower,upper,initcap,concat,concat_ws,lit,substring,col,format_string,lpad #Import string transformation functions
import json

#Get spark session
def get_spark_session(app_name):
    return SparkSession.builder.appName(app_name).getOrCreate()

#Read URL sending HTTP request - REST API
def get_http_response(url):

    response = requests.get(url)
    #response.raise_for_status()
    return response

def load_dataframe_to_db(clean_dataframe):

    from config import db
    db_user = db.get('DATABASE_USER')
    db_pass = db.get('DATABASE_PASSWORD')

    # Map Schema - Would like to research more on how to change some data types to enum, it was giving error while mapping to enum
    schema = "Application_ID varchar(8), Application_Status char(1), Credit_History int, Dependents char(2), Education varchar(12), Gender varchar(6), Income varchar(6), Married varchar(3), Property_Area varchar(10), Self_Employed varchar(3)"

    # Note: Default write mode is 'overwrite' which deletes the table and recreates it
    clean_dataframe.select("*").write.format("jdbc") \
    .option("url", "jdbc:mysql://localhost:3306/creditcard_capstone") \
    .option("dbtable", "creditcard_capstone.CDW_SAPP_loan_application") \
    .option("user", db_user) \
    .option("password", db_pass) \
    .option("truncate", "true") \
    .mode("overwrite") \
    .option("header","false") \
    .option("createTableColumnTypes", schema) \
    .save()


# STARTS the process
#url = 'https://httpbin.org/status/404'
url = 'https://raw.githubusercontent.com/platformps/LoanDataset/main/loan_data.json'
response = ''
try:
    response = get_http_response(url)
    print('HTTP Request Status: ',response.status_code)
    print('\nStatus Message: ',response.reason)
except requests.exceptions.HTTPError as http_error:
    print('HTTP Request Status: ',http_error.response.status_code)
    print('\nStatus Message: ',http_error.response.reason)

if(response):
    spark = get_spark_session('ETL_Card_Application')

    # Get json encoded content of response object. response.text is a str object
    json_data = response.json()

    #response.json()
    #print(spark.sparkContext.getConf().getAll())


    # schema_loan_app = StructType([ \
    #                             StructField("Application_Id",StringType(),True), \
    #                             StructField("Application_Status",StringType(),True), \
    #                             StructField("Credit_History",BooleanType(),True), \
    #                             StructField("Dependents",StringType(),True), \
    #                             StructField("Education", StringType(), True), \
    #                             StructField("Gender", StringType(), True), \
    #                             StructField("Income", StringType(), True), \
    #                             StructField("Married", StringType(), True), \
    #                             StructField("Property_Area", StringType(), True), \
    #                             StructField("Self_Employed", StringType(), True) \
    #                         ])
    
    # Changes json data to RDDs
    dataframe = spark.sparkContext.parallelize(json_data)

    # Reading multiline json, no json file is provided so created rdds to read it and transform it to dataframe
    dataframe = spark.read.json(dataframe)

    # Load data to table
    load_dataframe_to_db(dataframe)