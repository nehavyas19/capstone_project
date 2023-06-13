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
        st.write('Database loaded with clean data')

st.button('Start ETL for Loan Application Dataset', on_click=etl,args=(True,))