import streamlit as st
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
import pandas as pd
import get_customer_details as cust

st.set_page_config(layout="wide")

# Functional Requirements 2.2.4
# 4) Used to display the transactions made by a customer between two dates. Order by year, month, and day in descending order.

with st.container():
    st.write('Functional Requirements 2.2.4')
    st.write(':arrow_forward: Transactions between two dates')
    cols = st.columns(4)
    with cols[0]:
        first_name = st.text_input('Customer First Name')
    with cols[1]:
        last_name = st.text_input('Customer Last Name')
    with cols[2]:
        start_date = st.date_input('Start Date')
    with cols[3]:
        end_date = st.date_input('End Date')

    result = cust.get_customer_transactions_by_date(first_name, last_name, start_date, end_date)
    
    #Change MYSQL results to pandas dataframe - Easy to add cols or hide index to show in tables.
    dataframe = pd.DataFrame(result,columns=['Credit Card', 'SSN', 'Transaction Id', 'Transaction Type', 'Transaction Value', 'Date'])
    
# Display mysql results in streamlit grid table format
gd = GridOptionsBuilder.from_dataframe(dataframe)
gd.configure_pagination(enabled=True,paginationAutoPageSize=True,paginationPageSize=20)
gd.configure_default_column(groupable=True)

gridOptions = gd.build()
grid_table = AgGrid(dataframe,gridOptions=gridOptions,theme='material')