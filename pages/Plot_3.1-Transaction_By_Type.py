import streamlit as st
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
import pandas as pd
import get_transaction_details as trans
import plotly.express as px

st.set_page_config(layout="wide")

# Functional Requirements 3.1.1
# 1) Find and plot which transaction type has a high rate of transactions.

with st.container():
    st.write('Functional Requirements 3.1.1')
    st.write(':arrow_forward: Plot which transaction type has a high rate of transactions')
    
    result = trans.get_all_transactions()
    
    #Change MYSQL results to pandas dataframe - Easy to add cols or hide index to show in tables.
    dataframe = pd.DataFrame(result,columns=['Transaction Type', 'Transaction Value By Type'])
    #dataframe.loc['Total','Transaction Value By Type'] = dataframe['Transaction Value By Type'].sum()

# Display mysql results in streamlit grid table format
gd = GridOptionsBuilder.from_dataframe(dataframe)
gd.configure_pagination(enabled=True,paginationAutoPageSize=True,paginationPageSize=20)
gd.configure_default_column(groupable=True)

gridOptions = gd.build()
grid_table = AgGrid(dataframe,gridOptions=gridOptions,theme='material')


#Using Plotly - Just to try
fig = px.pie(values=dataframe['Transaction Value By Type'], names=dataframe['Transaction Type'], title='Transaction values by transaction type')
st.plotly_chart(fig)