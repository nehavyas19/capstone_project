def get_mysql_connection(db_name):
    #Connect to mysql database

    import mysql.connector
    from mysql.connector import errorcode
    from config import db

    #Get DB user/pwd
    db_user = db.get('DATABASE_USER')
    db_pass = db.get('DATABASE_PASSWORD')
    
    try:
        mysql_connect = mysql.connector.connect(host='localhost', user=db_user, password=db_pass,database=db_name)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    #else:
    #mysql_connect.close()

    return mysql_connect



def get_transaction_by_zip(zip, timeid):

    mysql_connect = get_mysql_connection('creditcard_capstone')
    cursor = mysql_connect.cursor(buffered=True)

    timeid = timeid+'%'
    query = (
                "SELECT c_cust.FIRST_NAME, c_cust.LAST_NAME, "
                "c_credit.BRANCH_CODE, c_credit.TRANSACTION_ID, c_credit.TRANSACTION_TYPE, c_credit.TRANSACTION_VALUE, c_credit.TIMEID, c_cust.CUST_ZIP "
                "FROM cdw_sapp_credit c_credit, cdw_sapp_customer c_cust " 
                "WHERE c_credit.TIMEID LIKE %s "
                "AND c_cust.CUST_ZIP = %s "
                "AND c_credit.CUST_SSN = c_cust.SSN "
                "ORDER BY c_credit.TRANSACTION_ID "
            )

    cursor.execute(query, (timeid, zip))
    result = cursor.fetchall()

    mysql_connect.close()

    return result


def get_transaction_by_type(transaction_type):

    mysql_connect = get_mysql_connection('creditcard_capstone')
    cursor = mysql_connect.cursor(buffered=True) #Buffered is needed for fetchall, otherwise it is lazy load and gives one result aat a time

    transaction_type = transaction_type+'%'
    query = (
                "SELECT transaction_type,count(*),SUM(TRANSACTION_VALUE) FROM cdw_sapp_credit c_credit " 
                "WHERE TRANSACTION_TYPE LIKE %s "
                "GROUP BY c_credit.TRANSACTION_TYPE"
            )

    cursor.execute(query, (transaction_type,)) #hmm, error. Had to use comma to give a tuple. String was not a valid input
    result = cursor.fetchall()

    mysql_connect.close()

    return result


def get_transaction_by_branch(state):

    mysql_connect = get_mysql_connection('creditcard_capstone')
    cursor = mysql_connect.cursor(buffered=True) #Buffered is needed for fetchall, otherwise it is lazy load and gives one result aat a time

    state = state+'%'
    query = (
                "SELECT count(*),SUM(c_credit.TRANSACTION_VALUE) as total FROM cdw_sapp_credit c_credit,cdw_sapp_branch c_branch "
                "WHERE (c_branch.BRANCH_STATE LIKE %s) "
                "AND c_branch.BRANCH_CODE = c_credit.BRANCH_CODE "
                "GROUP BY c_branch.BRANCH_STATE "
                "ORDER BY total DESC "
            )

    cursor.execute(query, (state,))
    result = cursor.fetchall()

    mysql_connect.close()

    return result


# Get transactions for plotting graphs - Requirement 3 - Data analysis and visualization

def get_all_transactions():

    mysql_connect = get_mysql_connection('creditcard_capstone')
    cursor = mysql_connect.cursor(buffered=True)

    query = (
                "SELECT transaction_type, round(sum(transaction_value),2) FROM cdw_sapp_credit c_credit "
                "GROUP BY TRANSACTION_TYPE "
                "ORDER BY sum(transaction_value) DESC "
            )

    cursor.execute(query)
    result = cursor.fetchall()

    mysql_connect.close()

    return result


def get_transaction_by_customer_top_10():

    mysql_connect = get_mysql_connection('creditcard_capstone')
    cursor = mysql_connect.cursor(buffered=True)

    query = (
                "SELECT c_cust.FIRST_NAME, c_cust.LAST_NAME, sum(c_credit.TRANSACTION_VALUE) as trans_total "
                "FROM cdw_sapp_credit c_credit, cdw_sapp_customer c_cust " 
                "WHERE c_credit.CUST_SSN = c_cust.SSN "
                "GROUP BY c_cust.FIRST_NAME, c_cust.LAST_NAME, c_cust.SSN "
                "ORDER BY trans_total DESC "
                "LIMIT 10 "
            )

    cursor.execute(query)
    result = cursor.fetchall()

    mysql_connect.close()

    return result