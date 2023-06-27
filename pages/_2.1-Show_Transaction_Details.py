import streamlit as st
import pandas as pd
import get_transaction_details as trans

st.set_page_config(
    page_title= 'Transaction Details',
    page_icon= ':credit_card:',
)
st.title('Transaction Details')
st.markdown("""
<style>
[data-baseweb="base-input"]{
background:#3399ff;
border: 2px;
border-radius: 3px;
}
</style>
""", unsafe_allow_html=True)


# Functional Requirements 2.1
# 1) Used to display the transactions made by customers living in a given zip code for a given month and year. Order by day in descending order.
with st.container():
    st.write('Functional Requirements 2.1.1')
    st.write(':arrow_forward: Transactions by customer zipcode, transaction month and year - Order by Day Desc')
    cols = st.columns(3)
    with cols[0]:
        zip_code = st.text_input('Zip Code')
    with cols[1]:
        transaction_month = st.selectbox(
        'Transaction Month',
        ('01','02','03','04','05','06','07','08','09','10','11','12'))
    with cols[2]:
        transaction_year = st.text_input(' Transaction Year')
        timeid = transaction_year+transaction_month

    result = trans.get_transaction_by_zip(zip_code, timeid)
    #Change MYSQL results to pandas dataframe - Easy to add cols and hide index.
    dataframe = pd.DataFrame(result,columns=['Customer First Name','Customer Last Name', 'Branch Code', 'Transaction Id', 'Transaction Type', 'Transaction Value', 'Date', 'Customer Zip'])

    # Display mysql results in streamlit table format

    # Custom table header color
    header_style = '''
        <style>
            table tbody tr:first-child td {
                background-color: orange;
            }
        </style>
    '''
    st.markdown(header_style, unsafe_allow_html=True)
    st.dataframe(dataframe,hide_index=True)


# Functional Requirements 2.2
# 2) Used to display the number and total values of transactions for a given type.

with st.container():
    st.write('Functional Requirements 2.1.2')
    st.write(':arrow_forward: Transactions by type')
    cols = st.columns(1)
    with cols[0]:
        transaction_type = st.text_input('Type')

    result = trans.get_transaction_by_type(transaction_type)
    dataframe = pd.DataFrame(result,columns=['Transaction Type','Number of transactions','Total value of transactions (USD)'])
    # Display mysql results as streamlit dataframe format
    st.dataframe(dataframe,hide_index=True)

# Functional Requirements 2.3
# 3) Used to display the total number and total values of transactions for branches in a given state.

with st.container():
    st.write('Functional Requirements 2.1.3')
    st.write(':arrow_forward: Transactions for branches by state - Order by Total Value Descending')
    cols = st.columns(1)
    with cols[0]:
        state = st.selectbox(
        'State',
        ('AL','AK','AZ','AR','CA','CO','CT','DE','DC','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','PR','RI','SC','SD','TN','TX','UT','VT','VA','VI','WA','WV','WI','WY'))

    result = trans.get_transaction_by_branch(state)
    dataframe = pd.DataFrame(result,columns=['Number of transactions','Total value of transactions (USD)'])
    # Display mysql results as streamlit dataframe format
    st.dataframe(dataframe,hide_index=True)