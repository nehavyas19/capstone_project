import db_connect as conn

def get_approved_app_for_self_employed():

    cursor = conn.mysql_connect.cursor(buffered=True)
    query = (
                "SELECT count(*) as cnt, Application_Status FROM cdw_sapp_loan_application "
                "WHERE Self_Employed = 'Yes' "
                "GROUP BY Application_Status "
                "ORDER BY cnt DESC "
            )

    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()

    return result


def get_rejections_for_married_male_apps():

    cursor = conn.mysql_connect.cursor(buffered=True)
    query = (
                "SELECT count(*) as cnt, Application_Status FROM cdw_sapp_loan_application "
                "WHERE Married = 'Yes' "
                "AND Gender = 'Male' "
                "GROUP BY Application_Status "
                "ORDER BY cnt DESC "
            )

    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()

    return result

#Fun fact - learned a Ctrl+Y command to Redo changes, apparently started making changes to this function instead of making a copy for a new feature
def get_top_3_months_highest_transactions():

    cursor = conn.mysql_connect.cursor(buffered=True)
    query = (
                "SELECT round(sum(transaction_value),2) as total_transaction_value, monthname(TIMEID) "
                "FROM cdw_sapp_credit "
                "GROUP BY monthname(TIMEID) "
                "ORDER BY total_transaction_value DESC "
                "LIMIT 3 "
            )

    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()

    return result


def get_branch_healthcare_max_total():

    cursor = conn.mysql_connect.cursor(buffered=True)
    query = (
                "SELECT round(sum(c_credit.transaction_value),2) as total_transaction_value, c_credit.branch_code, c_branch.branch_name "
                "FROM cdw_sapp_credit c_credit, cdw_sapp_branch c_branch "
                "WHERE TRANSACTION_TYPE = 'Healthcare' "
                "GROUP BY branch_code, branch_name "
                "ORDER BY total_transaction_value DESC "
                "LIMIT 5"
            )

    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()

    return result