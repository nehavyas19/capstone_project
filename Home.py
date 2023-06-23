import streamlit as st
import subprocess

st.set_page_config(
    page_title= 'Cap Stone Project Home Page',
    page_icon= ':house:',
)
st.title('Home page')

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