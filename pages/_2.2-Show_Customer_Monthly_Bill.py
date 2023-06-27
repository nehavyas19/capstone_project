import streamlit as st
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
import pandas as pd
import get_customer_details as cust

st.set_page_config(layout="wide")

# Functional Requirements 2.2.3
# 1) Generate month bill.

with st.container():
    st.write('Functional Requirements 2.2.3')
    st.write(':arrow_forward: Monthly bill by credit card')
    cols = st.columns(3)
    with cols[0]:
        credit_card = st.text_input('Credit Card')
    with cols[1]:
        year = st.text_input('Year')
    with cols[2]:
        month = st.selectbox('Month',('01','02','03','04','05','06','07','08','09','10','11','12'))

    result = cust.get_customer_monthly_bill(credit_card, month, year)
    
    #Change MYSQL results to pandas dataframe - Easy to add cols or hide index to show in tables.
    dataframe = pd.DataFrame(result,columns=['First Name', 'Last Name', 'Credit Card', 'Transaction Id', 'Transaction Type', 'Transaction Value (USD)'])
    dataframe.loc['Total','Transaction Value (USD)'] = dataframe['Transaction Value (USD)'].sum() # Add transaction total row in the end only for last column. Row index is 'Total'

# Display mysql results in streamlit grid table format
gd = GridOptionsBuilder.from_dataframe(dataframe)
gd.configure_pagination(enabled=True,paginationAutoPageSize=True,paginationPageSize=20)
gd.configure_default_column(groupable=True)

gridOptions = gd.build()
grid_table = AgGrid(dataframe,gridOptions=gridOptions,theme='material')