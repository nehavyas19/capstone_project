import streamlit as st
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
import pandas as pd
import get_customer_details as cust
import plotly.express as px

st.set_page_config(layout="wide")

# Functional Requirements 3.1.1
# 1) Find and plot which state has a high number of customers.

with st.container():
    st.write('Functional Requirements 3.1.1')
    st.write(':arrow_forward: Find and plot which state has a high number of customers.')
    
    result = cust.get_customers_by_state()
    
    #Change MYSQL results to pandas dataframe - Easy to add cols or hide index to show in tables.
    dataframe = pd.DataFrame(result,columns=['State', '# of Customers'])

# Display mysql results in streamlit grid table format
gd = GridOptionsBuilder.from_dataframe(dataframe)
gd.configure_pagination(enabled=True,paginationAutoPageSize=True,paginationPageSize=20)
gd.configure_default_column(groupable=True)

gridOptions = gd.build()
grid_table = AgGrid(dataframe,gridOptions=gridOptions,theme='material')


#Using Plotly - Just to try
fig = px.bar(x=dataframe['State'], y=dataframe['# of Customers'], title='Number Of Customers By State',labels={'x':'State','y':'# of Customers'})
st.plotly_chart(fig)