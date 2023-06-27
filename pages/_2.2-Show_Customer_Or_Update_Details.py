import streamlit as st
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
import pandas as pd
import get_customer_details as cust

st.set_page_config(layout="wide")
st.header('Display/Edit Customer Details. Click one checkbox at a time to update selected customer details.')

# Functional Requirements 2.2.1
# 1) Used to check the existing account details of a customer.

# Functional Requirements 2.2.2
# 2) Used to modify the existing account details of a customer.

result = cust.get_customer_account()
    
#Change MYSQL results to pandas dataframe - Easy to add cols or hide index to show in tables.
dataframe = pd.DataFrame(result,columns=['First Name','Middle Name', 'Last Name', 'Address', 'City', 'State', 'Zip', 'Country', 'Phone', 'Email', 'SSN', 'Credit Card'])

# Display mysql results in streamlit grid table format
gd = GridOptionsBuilder.from_dataframe(dataframe)
gd.configure_pagination(enabled=True,paginationAutoPageSize=True,paginationPageSize=20)
gd.configure_default_column(editable=True)
gd.configure_selection(selection_mode='single', use_checkbox=True)
gd.configure_column("Credit Card",editable=False)
gd.configure_column("SSN",editable=False)

gridOptions = gd.build()

#{'STREAMLIT': <AgGridTheme.STREAMLIT: 'streamlit'>, 'ALPINE': <AgGridTheme.ALPINE: 'alpine'>, 'BALHAM': <AgGridTheme.BALHAM: 'balham'>, 'MATERIAL': <AgGridTheme.MATERIAL: 'material'>}
grid_table = AgGrid(dataframe,gridOptions=gridOptions,theme='material')    
updated_dataframe = grid_table['selected_rows']

if updated_dataframe:
    update_data = (
                    updated_dataframe[0]['First Name'],
                    updated_dataframe[0]['Middle Name'],
                    updated_dataframe[0]['Last Name'],
                    updated_dataframe[0]['Address'],
                    updated_dataframe[0]['City'],
                    updated_dataframe[0]['State'],
                    updated_dataframe[0]['Zip'],
                    updated_dataframe[0]['Country'],
                    updated_dataframe[0]['Phone'],
                    updated_dataframe[0]['Email'],
                    updated_dataframe[0]['SSN'],
                  )
    cust.edit_customer_account(update_data)
