import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import hydralit_components as hc
from streamlit_elements import nivo, elements, mui, html
from grist_api import GristDocAPI
import requests
import json
import streamlit as st
import numpy as np
import json
import time
import hmac

# Login form to check the password
def check_password():
    """Returns `True` if the user had a correct password."""

    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["username"] in st.secrets[
            "passwords"
        ] and hmac.compare_digest(
            st.session_state["password"],
            st.secrets.passwords[st.session_state["username"]],
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the username or password.
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    # Return True if the username + password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show inputs for username + password.
    login_form()
    if "password_correct" in st.session_state:
        st.error("😕 User not known or password incorrect")
    return False


if not check_password():
    st.stop()


# Set the page title and favicon of the app
st.set_page_config(layout='wide', initial_sidebar_state='collapsed')
custom_html = """
<div class="banner">
    <img src="https://github.com/ArthurSrz/forge-data-position-final/blob/main/resource/logo_forge_vf.png?raw=true" alt="Banner Image">
</div>
<style>
    .banner {
        width: 100%;
        height: 150px;
        display: flex;
        justify-content: center;
        align-items: center;
        overflow: hidden;
        padding: 10px;
        
    }
    .banner img {
        max-width: 100%;
        max-height: 100%;
    }
</style>
"""

# Display the custom HTML
st.components.v1.html(custom_html)



# Set up the Grist API connection to the Grist document
SERVER = "https://docs.getgrist.com"
DOC_ID = "nSV5r7CLQCWzKqZCz7qBor"
API_KEY = st.secrets["grist_api_key"]

## Initialize GristDocAPI with document ID, server, and API key
api = GristDocAPI(DOC_ID, server=SERVER, api_key=API_KEY)

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

# Load Grist tables corresponding to the existing Data Position

## Load Data Position Maitre (Form3 from Grist)
subdomain = "docs"
doc_id = "nSV5r7CLQCWzKqZCz7qBor"
table_id_3 = "Form3"
url = f"https://{subdomain}.getgrist.com/api/docs/{doc_id}/tables/{table_id_3}/records"
response = requests.get(url, headers=headers)
if response.status_code == 200:
    data2 = response.json()
    columns = data2['records'][0]['fields'].keys()
    # Process the data as needed
else:
    print(f"Request failed with status code {response.status_code}")

## ADD NEW DATA POSITION HERE

#create a function to add config_info to the config data table on Grist
def add_config(df_config):
    ## Convert DataFrame to list of records
    records = [{"fields": {"table_id": record["table_id"], "profiles": ", ".join(record["profiles"])}} for record in df_config.to_dict(orient='records')]
    ## Prepare the request body
    data = {"records": records}
    
    docId = "nSV5r7CLQCWzKqZCz7qBor"
    tableId = "Config"
    
    ## Use the Grist API to add the new rows to the specified Grist table
    url = f"https://{subdomain}.getgrist.com/api/docs/{docId}/tables/{tableId}/records"
    response = requests.post(url, headers=headers, json=data) 


# generate the different tabs of the app
menu_data = [
    {'icon': "far fa-copy", 'label': "Qualification"}
]

## Set the default tab of the app to "Qualification"
if 'selected_tab' not in st.session_state:
    st.session_state.selected_tab = "Qualification"

#initialize selected_data in session state.
if 'selected_data' not in st.session_state:
    st.session_state.selected_data = {}



## Create a colorizer tab
def colorizer_tab():
    
    st.title("Bienvenue dans le Data Position Studio")
    st.markdown("Vous avez maintenant la possibilité d'utiliser les Data Position déja créés par la communauté de Datactivist pour identifier quel est votre profil data ou ceux au sein de votre organisation.")
    
    #Create empty containers for space
    container = st.container(border=False)
    container.write("")
    container.write("")
    container.write("")
    container.write("")
    
    
    
    st.header("Liste des Data Position de la communauté")
    col1, col2, col3 = st.columns(3)
    
    
        
        
    
    # Create elements with the different data positions that can be used
    with col1:
        with st.container(border=True):
            st.text("Data Position Maitre")
            expander = st.expander("Description")
            expander.write("Le Data Position par défaut créé par Datactivist")
            #make checkboxes where the users get to choose which profile he is going to evaluate
            profiles = st.multiselect(
                "Choix des profils",["Data Analyst", "Data Scientist", "Machine Learning Engineer", "Geomaticien", "Data Engineer", "Data Protection Officer", "Chef de Projet Data"],max_selections=20)      
            if st.button("Charger le data position",type="primary", key=1):
                st.session_state.profiles = profiles
                st.session_state.selected_data = data2
                st.session_state.table_id = table_id_3
                
                subdomain = "docs"
                docId = "nSV5r7CLQCWzKqZCz7qBor"
                tableId = "Config"
                url = f"https://{subdomain}.getgrist.com/api/docs/{docId}/tables/{tableId}/records"
                response = requests.get(url, headers=headers)
                #st.write(response.json())
                if response.status_code == 200:
                    tables = response.json()
                
                
                
                df_config = pd.DataFrame({'table_id': table_id_3, 'profiles': [profiles]})
                #st.dataframe(df_config)
                #send data to the config grist
                add_config(df_config)
                st.success("Data position chargé 🚚")
                
    with col2:
        with st.container(border=True):
            st.text("Data Position en cours de création")
            
    with col3:
        with st.container(border=True):
            st.text("Data Position en cours de création")
            
    
      
    #Create empty containers for space
    container = st.container(border=False)
    container.write("")
    container.write("")
    container.write("")
    container.write("")
    container.write("")
    
    
    
    col1, col2 = st.columns(2)
    
    ## Create a storage where the data will be stored dynamically
    if 'data' not in st.session_state:
        st.session_state.data = {
            'profile_type':[],
            'question': [],
            'reponse': [],
            'score': []
        }    
        st.session_state.data['reponse'] = []

    

# Create a function to display the selected tab content
def display_tab_content(tab_label):
    if tab_label == "Qualification":
        colorizer_tab()
    elif tab_label == "Recrutement":
        gatherizer_tab()
    elif tab_label == "Position":
        dispenser_tab()

# Theme of the page
over_theme = {'txc_inactive': 'white','menu_background':'#1c3f4b','txc_active':'#e95459','option_active':''}

# Create the navigation bar
menu_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    #home_name='Home',
    #login_name='Logout',
    hide_streamlit_markers=False,
    sticky_nav=True,
    sticky_mode='pinned'
)

# Get the selected tab label from the menu
selected_tab_label = menu_id

# Display the selected tab content
display_tab_content(selected_tab_label)


# Store the selected tab in the session state
if selected_tab_label != st.session_state.selected_tab:
    st.session_state.selected_tab = selected_tab_label


