import streamlit as st
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
import pandas as pd
import get_transaction_details as trans
import plotly.express as px

st.set_page_config(layout="wide")

# Functional Requirements 3.1.3
# 1) Find and plot the sum of all transactions for the top 10 customers, and which customer has the highest transaction amount.

with st.container():
    st.write('Functional Requirements 3.1.3')
    st.write(':arrow_forward: Find and plot the sum of all transactions for the top 10 customers, and which customer has the highest transaction amount.')
    
    result = trans.get_transaction_by_customer_top_10()
    
    #Change MYSQL results to pandas dataframe - Easy to add cols or hide index to show in tables.
    dataframe = pd.DataFrame(result,columns=['First Name', 'Last Name', 'Transactions Total'])

# Display mysql results in streamlit grid table format
gd = GridOptionsBuilder.from_dataframe(dataframe)
gd.configure_pagination(enabled=True,paginationAutoPageSize=True,paginationPageSize=20)
gd.configure_default_column(groupable=True)

gridOptions = gd.build()
grid_table = AgGrid(dataframe,gridOptions=gridOptions,theme='material')


#Using Plotly - Just to try
fig = px.bar(x=dataframe['First Name']+' '+dataframe['Last Name'], y=dataframe['Transactions Total'], title='Top 10 Customers - Total of all transactions',labels={'x':'Customer Name','y':'Total Transactions Value'})
st.plotly_chart(fig)