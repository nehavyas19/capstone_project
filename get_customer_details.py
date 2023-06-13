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

def get_customer_account():

    mysql_connect = get_mysql_connection('creditcard_capstone')
    cursor = mysql_connect.cursor(buffered=True)
    query = (
                "SELECT first_name, middle_name, last_name, full_street_address, cust_city, cust_state, cust_zip, cust_country, cust_phone, cust_email, ssn, c_cust.credit_card_no "
                "FROM cdw_sapp_customer c_cust "
                "ORDER BY c_cust.first_name "
            )
    cursor.execute(query)
    result = cursor.fetchall()

    mysql_connect.close()

    return result


def edit_customer_account(updated_data):
    
    mysql_connect = get_mysql_connection('creditcard_capstone')
    cursor = mysql_connect.cursor(buffered=True)

    query = (
                """UPDATE cdw_sapp_customer SET first_name = %s, middle_name = %s, last_name = %s, full_street_address = %s, cust_city = %s, cust_state = %s, cust_zip = %s, cust_country = %s, cust_phone = %s, cust_email = %s WHERE SSN = %s"""
            )
    
    cursor.execute(query,updated_data)
    mysql_connect.commit()
    mysql_connect.close()


def get_customer_monthly_bill(credit_card,month,year):

    mysql_connect = get_mysql_connection('creditcard_capstone')
    cursor = mysql_connect.cursor(buffered=True)

    timeid = year+month+'%'
    query = (
                "SELECT c_cust.first_name, c_cust.last_name, c_cust.credit_card_no, "
                "c_credit.transaction_id, c_credit.transaction_type, c_credit.transaction_value "
                "FROM cdw_sapp_customer c_cust, cdw_sapp_credit c_credit "
                "WHERE c_cust.ssn = c_credit.cust_ssn "
                "AND c_credit.credit_card_no = c_cust.credit_card_no "
                "AND c_credit.credit_card_no = %s "
                "AND c_credit.timeid LIKE %s "
                "ORDER BY c_credit.transaction_id "
            )
    cursor.execute(query,(credit_card,timeid))
    result = cursor.fetchall()

    mysql_connect.close()

    return result


def get_customer_transactions_by_date(first_name, last_name, start_date, end_date):

    mysql_connect = get_mysql_connection('creditcard_capstone')
    cursor = mysql_connect.cursor(buffered=True)

    query = (
                "SELECT c_credit.credit_card_no, c_credit.cust_ssn, "
                "c_credit.transaction_id, c_credit.transaction_type, c_credit.transaction_value, c_credit.timeid "
                "FROM cdw_sapp_customer c_cust, cdw_sapp_credit c_credit "
                "WHERE c_cust.ssn = c_credit.cust_ssn "
                "AND c_cust.first_name = %s "
                "AND c_cust.last_name = %s "
                "AND CAST(c_credit.timeid as DATE) BETWEEN %s AND %s "
                "ORDER BY CAST(c_credit.timeid as DATE) "
            )
    
    cursor.execute(query,(first_name, last_name, start_date, end_date))
    result = cursor.fetchall()

    mysql_connect.close()

    return result


def get_customers_by_state():

    mysql_connect = get_mysql_connection('creditcard_capstone')
    cursor = mysql_connect.cursor(buffered=True)

    query = (
                "SELECT cust_state, count(*) as customer_cnt "
                "FROM cdw_sapp_customer "
                "GROUP BY cust_state "
                "ORDER BY customer_cnt DESC "
            )
    
    # query = (
    #             "SELECT c_branch.branch_code, count(SSN) as customer_cnt "
    #             "FROM cdw_sapp_customer c_cust, cdw_sapp_credit c_credit, cdw_sapp_branch c_branch "
    #             "WHERE c_credit.branch_code = c_branch.branch_code "
    #             "AND c_credit.cust_ssn = c_cust.ssn "
    #             "GROUP BY c_branch.branch_code "
    #             "ORDER BY customer_cnt DESC "
    #         )

    cursor.execute(query)
    result = cursor.fetchall()

    mysql_connect.close()

    return result