# Import all the necessary libraries
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, VarcharType, TimestampType, DoubleType
from pyspark.sql.functions import lower,upper,initcap,concat,concat_ws,lit,substring,col,format_string,lpad #Import string transformation functions

# Get the spark session started, if already exists returns that
def get_spark_session(app_name):
    return SparkSession.builder.appName(app_name).getOrCreate()

# Read the json file to the spark dataframe
def load_file_to_dataframe(spark,file,schema):

    dataframe = spark.read.schema(schema).json(file)

    return dataframe

# Transform customer details
# Transforms usual string transformations, drops 2 columns after concatenation, changes customer phone to add 123 - just to make it 10 digit
# Adding anything to customer phone is not guaranteed to give correct # and is an overkill, state codes can be different, customer changes state and keeps the #s
def transform_customer(dataframe):
    transformed_dataframe = dataframe.withColumn('FIRST_NAME',initcap(dataframe['FIRST_NAME'])) \
                                     .withColumn('MIDDLE_NAME',lower(dataframe['MIDDLE_NAME'])) \
                                     .withColumn('LAST_NAME',initcap(dataframe['LAST_NAME'])) \
                                     .withColumn('FULL_STREET_ADDRESS',concat_ws(',',dataframe['APT_NO'],dataframe['STREET_NAME'])) \
                                        .drop('APT_NO') \
                                        .drop('STREET_NAME') \
                                     .withColumn("CUST_ZIP",col("CUST_ZIP").cast("int")) \
                                     .withColumn('CUST_PHONE',lpad(dataframe['CUST_PHONE'],10,'123')) \
                                     .withColumn('CUST_PHONE',
                                                   concat(
                                                   lit('('),
                                                   substring(col('CUST_PHONE'),1,3), # Use col() function - return a column, col() refers to different internal function than dataframe['column']. Most of the times they are same
                                                   lit(')'),
                                                   substring(col('CUST_PHONE'),4,3),
                                                   lit('-'),
                                                   substring(col('CUST_PHONE'),7,4)
                                                   )
                                                ) 
    #Note - Customer zip is in double quotes vs branch zip is not, so struct field is string for one and int for the other
    #Note - Customer zip is direct move so did not add 0 to it to make it 5 digit
    transformed_dataframe.collect()
    return transformed_dataframe

# Transforms credit details
# Concats 4 digit year, 2 digit month, 2 digit day to new field TIMEID and drops all the unnecessary columns
# Removes a 'Test' transaction type
def transform_credit(dataframe):
    transformed_dataframe = dataframe.withColumn('TIMEID',concat(format_string("%04d",col('YEAR').cast('int')),format_string("%02d",col('MONTH').cast('int')),format_string("%02d",col('DAY').cast('int')))) \
                                        .drop('DAY') \
                                        .drop('MONTH') \
                                        .drop('YEAR') 
    
    # Remove data containing 'Test' transaction type
    transformed_dataframe = transformed_dataframe[(transformed_dataframe.TRANSACTION_TYPE != 'Test')]
    
    transformed_dataframe.collect()
    return transformed_dataframe

# Transforms branch details
# Fills zipcode with 999999 where zipcode is null
def transform_branch(dataframe):
    #Note - col function works on chained value vs dataframe['column_name'] does not. Phone was giving errors when changed after adding padded values
    transformed_dataframe = dataframe.fillna(value=999999,subset=['BRANCH_ZIP']) \
                                     .withColumn('BRANCH_ZIP',concat(format_string("%05d",col('BRANCH_ZIP')))) \
                                     .withColumn('BRANCH_PHONE',
                                                   concat(
                                                   lit('('),
                                                   substring(col('BRANCH_PHONE'),1,3),
                                                   lit(')'),
                                                   substring(col('BRANCH_PHONE'),4,3),
                                                   lit('-'),
                                                   substring(col('BRANCH_PHONE'),7,4)
                                                   )
                                                )
    transformed_dataframe.collect()
    return transformed_dataframe

# Loads the clean dataframe to database
def load_dataframe_to_db(clean_dataframe, table_name, schema):

    from config import db
    db_user = db.get('DATABASE_USER')
    db_pass = db.get('DATABASE_PASSWORD')

    schema_transform_branch = "BRANCH_NAME varchar(25), BRANCH_STREET varchar(50), BRANCH_CITY varchar(50), BRANCH_STATE varchar(2), BRANCH_PHONE varchar(15), BRANCH_ZIP int, LAST_UPDATED timestamp"
    schema_transform_credit = "TIMEID varchar(8), CREDIT_CARD_NO varchar(16), TRANSACTION_TYPE varchar(25)"
    schema_transform_customer = "FIRST_NAME varchar(50), MIDDLE_NAME varchar(50), LAST_NAME varchar(50), CREDIT_CARD_NO varchar(16), FULL_STREET_ADDRESS varchar(200), CUST_CITY varchar(50), CUST_STATE varchar(2), CUST_COUNTRY varchar(25), CUST_PHONE varchar(13), CUST_EMAIL varchar(50)"


    #Note: Write mode is 'overwrite' which drops the table and recreates it
    # Schema is created to map the dataframes to mysql types.
    clean_dataframe.select("*").write.format("jdbc") \
    .option("url", "jdbc:mysql://localhost:3306/creditcard_capstone") \
    .option("dbtable", "creditcard_capstone."+table_name) \
    .option("user", db_user) \
    .option("password", db_pass) \
    .option("truncate", "true") \
    .mode("overwrite") \
    .option("header","false") \
    .option("createTableColumnTypes", locals()[schema]) \
    .save()


# Get the spark session
spark = get_spark_session('ETL_Loan_Application')

# File lists to extract, transform and load
file_list = {
                'transform_branch':'data_sets/cdw_sapp_branch.json',
                'transform_credit':'data_sets/cdw_sapp_credit.json',
                'transform_customer':'data_sets/cdw_sapp_customer.json'
            }

schema_transform_branch = StructType([ \
                                    StructField("BRANCH_CODE",IntegerType(),True), \
                                    StructField("BRANCH_NAME",StringType(),True), \
                                    StructField("BRANCH_STREET",StringType(),True), \
                                    StructField("BRANCH_CITY", StringType(), True), \
                                    StructField("BRANCH_STATE", StringType(), True), \
                                    StructField("BRANCH_ZIP", IntegerType(), True), \
                                    StructField("BRANCH_PHONE", StringType(), True), \
                                    StructField("LAST_UPDATED", TimestampType(), True) \
                                ])

schema_transform_credit = StructType([ \
                                StructField("TRANSACTION_ID",IntegerType(),True), \
                                StructField("DAY",StringType(),True), \
                                StructField("MONTH",StringType(),True), \
                                StructField("YEAR",StringType(),True), \
                                StructField("CREDIT_CARD_NO", StringType(), True), \
                                StructField("CUST_SSN", IntegerType(), True), \
                                StructField("BRANCH_CODE", IntegerType(), True), \
                                StructField("TRANSACTION_TYPE", StringType(), True), \
                                StructField("TRANSACTION_VALUE", DoubleType(), True) \
                            ])

schema_transform_customer = StructType([ \
                                StructField("FIRST_NAME",StringType(),True), \
                                StructField("MIDDLE_NAME",StringType(),True), \
                                StructField("LAST_NAME",StringType(),True), \
                                StructField("SSN",IntegerType(),True), \
                                StructField("CREDIT_CARD_NO", StringType(), True), \
                                StructField("APT_NO", StringType(), True), \
                                StructField("STREET_NAME", StringType(), True), \
                                StructField("CUST_CITY", StringType(), True), \
                                StructField("CUST_STATE", StringType(), True), \
                                StructField("CUST_COUNTRY", StringType(), True), \
                                StructField("CUST_ZIP", StringType(), True), \
                                StructField("CUST_PHONE", StringType(), True), \
                                StructField("CUST_EMAIL", StringType(), True), \
                                StructField("LAST_UPDATED", TimestampType(), True) \
                            ])


#ETL Starts
for file_transform, file_path in file_list.items():
    
    schema = 'schema_'+str(file_transform) #Generate dynamic variable to get runtime schema using locals()
    dataframe = load_file_to_dataframe(spark, file_path, locals()[schema])
    clean_dataframe = locals()[file_transform](dataframe) #locals used to call function in local scope or it parses it as string

    table_name = file_path.partition('/')[2].partition('.')[0]
    load_dataframe_to_db(clean_dataframe, table_name, schema)