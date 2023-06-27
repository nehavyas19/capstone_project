import streamlit as st
import subprocess

st.set_page_config(
    page_title= 'Cap Stone Project Home Page',
    page_icon= ':house:',
)
st.title('Home page')

st.header('What is the project all about?')
st.markdown('Manage ETL for Credit Card and Loan Application Data Sets with a goal to perform analyzing and visualization of data')
st.markdown('Some goals are -')
st.markdown('See how branches are performing across USA')
st.markdown('See where customers are spending more money')
st.markdown('See and update customer accounts as necessary')
st.markdown('Get clarity on who is applying for loans and what are the criteria to approve/reject loans')

st.header('Tools used to complete the project?')
st.markdown('1. Pyspark to read and transform credit card data sets')
st.markdown('2. Requests module to read rest API and get response code and data for loan application data set')
st.markdown('3. MySQL to load the clean data to retrieve, analyse and visualize at anytime point of time')
st.markdown('4. Streamlit to display and interact with the data in user-friendly way')
st.markdown('5. Plotly library and Tableau to create viz')
st.markdown('6. Logging module to log ETL for credit card dataset in a log file')


st.header('Run ETLs on data sets')
def etl(run_etl):
    if(run_etl == True):
        subprocess.run(['python','etl.py'])
        st.write('Database loaded with clean data - Credit Card')

st.button('Start ETL for Credit Card Dataset', on_click=etl,args=(True,))


def etl_loan(run_etl):
    if(run_etl == True):
        response = subprocess.run(['python','etl_loan.py'],capture_output=True,text=True)
        st.write(response.stdout)
        st.write('Database loaded with clean data - Loan Application')

st.button('Start ETL for Loan Application Dataset', on_click=etl_loan,args=(True,))