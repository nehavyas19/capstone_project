import streamlit as st
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
import pandas as pd
import get_loan_details as loan_app
import plotly.express as px

st.set_page_config(layout="wide")

# Functional Requirements 5.1
# 1) Find and plot which transaction type has a high rate of transactions.

with st.container():
    st.write('Functional Requirements 5.1')
    st.write(':arrow_forward: Find and plot the percentage of applications approved for self-employed applicants.')
    
    result = loan_app.get_approved_app_for_self_employed()
    
    #Change MYSQL results to pandas dataframe - Easy to add cols or hide index to show in tables.
    dataframe = pd.DataFrame(result,columns=['# of Applications', 'Approval Status'])

# Display mysql results in streamlit grid table format
gd = GridOptionsBuilder.from_dataframe(dataframe)
gd.configure_pagination(enabled=True,paginationAutoPageSize=True,paginationPageSize=20)
gd.configure_default_column(groupable=True)

gridOptions = gd.build()
grid_table = AgGrid(dataframe,gridOptions=gridOptions,theme='material')


#Using Plotly - Just to try
fig = px.pie(values=dataframe['# of Applications'], names=dataframe['Approval Status'], title='Percentage of approved applications for Self-Employed applicants', color_discrete_sequence=["green","red"])
fig.update_traces(pull=[0.1]) #Lets pull a slice out
st.plotly_chart(fig)



# Functional Requirements 5.2
# 1) Find the percentage of rejection for married male applicants.

with st.container():
    st.write('Functional Requirements 5.2')
    st.write(':arrow_forward: Find the percentage of rejection for married male applicants.')
    
    result = loan_app.get_rejections_for_married_male_apps()
    
    #Change MYSQL results to pandas dataframe - Easy to add cols or hide index to show in tables.
    dataframe = pd.DataFrame(result,columns=['# of Applications', 'Approval Status'])

# Display mysql results in streamlit grid table format
gd = GridOptionsBuilder.from_dataframe(dataframe)
gd.configure_pagination(enabled=True,paginationAutoPageSize=True,paginationPageSize=20)
gd.configure_default_column(groupable=True)

gridOptions = gd.build()
grid_table = AgGrid(dataframe,gridOptions=gridOptions,theme='material')


#Using Plotly - Just to try
color_discrete_sequence = ['green']*len(dataframe)
color_discrete_sequence[1] = 'red'


dataframe['percentage'] = round((dataframe['# of Applications'] / dataframe['# of Applications'].sum()) * 100)
fig = px.bar(dataframe, x=dataframe['Approval Status'], y=dataframe['# of Applications'], text=dataframe['percentage'].map(lambda x:str(x)+' %'), color='Approval Status', color_discrete_sequence=color_discrete_sequence, title='Find the percentage of rejection for married male applicants.')
st.plotly_chart(fig)



# Functional Requirements 5.3
# 1) Find and plot the top three months with the largest transaction data.

with st.container():
    st.write('Functional Requirements 5.3')
    st.write(':arrow_forward: Find and plot the top three months with the largest transaction data.')
    
    result = loan_app.get_top_3_months_highest_transactions()
    
    #Change MYSQL results to pandas dataframe - Easy to add cols or hide index to show in tables.
    dataframe = pd.DataFrame(result,columns=['Total Transactions Value', 'Months(All the data of 2018)'])

# Display mysql results in streamlit grid table format
gd = GridOptionsBuilder.from_dataframe(dataframe)
gd.configure_pagination(enabled=True,paginationAutoPageSize=True,paginationPageSize=20)
gd.configure_default_column(groupable=True)

gridOptions = gd.build()
grid_table = AgGrid(dataframe,gridOptions=gridOptions,theme='material')


#Using Plotly - Just to try
fig = px.bar(dataframe, x=dataframe['Months(All the data of 2018)'], y=dataframe['Total Transactions Value'], title='Top three months with the largest transaction data.')
fig.update_layout(yaxis_range=[dataframe['Total Transactions Value'].min()-100,dataframe['Total Transactions Value'].max()])
st.plotly_chart(fig)


# Functional Requirements 5.4
# 1) Find and plot which branch processed the highest total dollar value of healthcare transactions.

with st.container():
    st.write('Functional Requirements 5.4')
    st.write(':arrow_forward: Find and plot which branch processed the highest total dollar value of healthcare transactions.')
    
    result = loan_app.get_branch_healthcare_max_total()
    
    #Change MYSQL results to pandas dataframe - Easy to add cols or hide index to show in tables.
    dataframe = pd.DataFrame(result,columns=['Total Transactions Value', 'Branch Code', 'Branch Name'])

# Display mysql results in streamlit grid table format
gd = GridOptionsBuilder.from_dataframe(dataframe)
gd.configure_pagination(enabled=True,paginationAutoPageSize=True,paginationPageSize=20)
gd.configure_default_column(groupable=True)

gridOptions = gd.build()
grid_table = AgGrid(dataframe,gridOptions=gridOptions,theme='material')


#Using Plotly - Just to try
dataframe = dataframe.iloc[:5]
dataframe['Branch Code'] = dataframe['Branch Code'].values.astype('str')
fig = px.line(dataframe, x=(dataframe['Branch Code']+'-'+dataframe['Branch Name']), y=dataframe['Total Transactions Value'], title='Branches with healthcare transaction totals')
fig.update_layout(xaxis_title='Bank Code-Bank Name')
fig.update_xaxes(showline=True, linewidth=2, linecolor='black')
fig.update_yaxes(showline=True, linewidth=2, linecolor='black')
st.plotly_chart(fig)

# list_df = []
# low = 0
# high = 10
# max = len(dataframe.index)

# while(high <= max):
#     list_df.append(dataframe['Total Transactions Value'].values[low:high])
#     low = high+1
#     high += 10

# fig = px.imshow(pd.DataFrame(list_df).transpose(), text_auto=True)
# st.plotly_chart(fig, use_container_width=True)