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

    
    
            
            # Mise à jour du DataFrame st.session_state.selected_data
            #if 'selected_data' not in st.session_state or not isinstance(st.session_state.selected_data, pd.DataFrame):
            #    st.session_state.selected_data = pd.DataFrame(columns=['profile_type', 'question', 'reponse', 'score'])

            #new_data = pd.DataFrame({'profile_type': [profile_type], 'question': [question], 'reponse': [reponse], 'score': [score]})
    
            # Assurez-vous que les colonnes sont dans le même ordre
            #new_data = new_data[st.session_state.selected_data.columns]

            #st.session_state.selected_data = pd.concat([st.session_state.selected_data, new_data], ignore_index=True)
            
            
            #json_records = st.session_state.selected_data.to_dict(orient='records')
            #json_data = {'records': json_records}
            #print("JSON is ")
            #print(json_data)
            #st.session_state.selected_data = json_data
            #st.session_state.table_id = table_id_0
            #st.success("Data added to Grist table")
            
        ## Button to add questions Google spreadsheet

        #if st.button("Ajouter", key=10):
        #    st.session_state.data['profile_type'].append(profile_type)
        #    st.session_state.data['question'].append(question)
        #    st.session_state.data['answer'].append(answer)
        #    st.session_state.data['score'].append(score)
        #    # Combine the existing data from Google Sheets and new data
        #    existing_data = conn.read(worksheet="Colorizer", usecols=["question","answer","score","profile_type"],ttl=0, nrows=10)
        #    existing_df = pd.DataFrame(existing_data)
        #    #st.write("Existing Data:")
        #    #st.dataframe(existing_df)
        #    new_df = pd.DataFrame(st.session_state.data)
        #    #st.write("New Data:")
        #    #st.dataframe(new_df)
        #    combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        #    #st.write("Combined Data:")
        #    #st.dataframe(combined_df)
        #    conn.update(worksheet="Colorizer", data=combined_df)
        #    st.success("Data added to Google Sheets")
        #    st.session_state.data = {
        #        'profile_type': [],
        #        'question': [],
        #        'answer': [],
        #        'score': []
        #    }
    
    
         
                    
## create a tab to gather the answers from the population to questions added to the database
def gatherizer_tab():
    #print(st.session_state)
    if 'table_id' not in st.session_state:
        st.warning("Veuillez charger un data position")
        return
    
    st.title("Recrutement des profils data")
    st.markdown("Bienvenue sur le formulaire de recrutement. Répondez aux questions pour valider votre candidature. Nous reviendrons vers vous très vite.")
    
    ## Check if there are data available loaded
    
    
    
    #print(st.session_state.selected_data)
    #if 'colorizer_data' in st.session_state:
    #    
    #    df_colorizer = st.session_state.colorizer_data
    #    st.session_state.selected_data = df_colorizer
    #    st.success("Données chargées depuis le DataFrame de session")

    
    
    ## create an empty dataframe to store the answers
    df_answers = pd.DataFrame(columns=['nom', 'prenom', 'mail', 'question', 'reponse', 'score','profile_type'])
    
    ## if grist was used, transform the json file into a dataframe
    grist_question_df = st.session_state.selected_data
    #print(grist_question_df['records'])
    records = grist_question_df['records']
    grist_question_df = pd.json_normalize(records, sep='_')
    ## clean the column names to display them in a nice way in the app

    grist_question_df.columns = [col.replace('fields_', '') for col in grist_question_df.columns]
    #print(grist_question_df)
    
    
    
    ## If google spreadsheet was chosen, add content from the google spreadsheet 
    #question_data = conn.read(worksheet="Colorizer", usecols=["question","answer","score","profile_type"],ttl=0, nrows=10)
    #spreadsheet_question_df = pd.DataFrame(question_data)
    
   
    grist_question_df = grist_question_df 
    
    
    
    #get the list of selected profils present in st.session_state.profiles
    selected_profiles = st.session_state.profiles

    ## from the database, select the screening questions
    introduction_question_df = grist_question_df[(grist_question_df.question_type == "screening") & (grist_question_df.profile_type.isin(selected_profiles))]
    unique_introduction_questions = introduction_question_df.question.unique()

    #from the data, filter only the expertise data related to the selected profiles
    unique_expertise_questions = grist_question_df[(grist_question_df.question_type == "expertise") & (grist_question_df.profile_type.isin(selected_profiles))]
    
    #from the data, filter only the mastery data related to the selected profiles
    unique_mastery_questions = grist_question_df[(grist_question_df.question_type == "mastery") & (grist_question_df.profile_type.isin(selected_profiles))]
    
    ## from the data, select the unique questions
    unique_questions = grist_question_df[grist_question_df.question_type == "expertise"].question.unique()
    unique_reponse = grist_question_df[grist_question_df.question_type == "expertise"].reponse.unique()
    
    
    ## create a form to get respondent name and email
    st.header("Qui êtes-vous ? :disguised_face:")
    nom = st.text_input("Nom", key='nom')
    prenom = st.text_input("Prenom", key='prenom')
    mail = st.text_input("Mail", key='mail')
    #append the values of the inputs to the df_answers
    # df_answers = df_answers.append({'nom': nom, 'prenom': prenom, 'mail': mail}, ignore_index=True)
    
    ## create a form to do some profiling
    st.header("Quel(s) profil(s) data êtes-vous ?:male-detective:")
    
    for i, question_people in enumerate(unique_introduction_questions):
        st.write(question_people)
        answer_people = st.selectbox("Votre réponse", grist_question_df[grist_question_df.question == question_people].reponse.unique(), index=None, key = i+1000)
        question_type = grist_question_df[grist_question_df.reponse == answer_people].question_type.values
        score = grist_question_df[grist_question_df.reponse == answer_people].score.values
        profile_type_vals = grist_question_df[grist_question_df.reponse == answer_people].profile_type.values
        profile_type_vals = profile_type_vals.tolist()
        df = pd.DataFrame({'nom': [nom], 'prenom': [prenom], 'mail': [mail],'question': [question_people],'question_type':[question_type], 'reponse': [answer_people],'score': [score],'profile_type':[profile_type_vals]})
        # Append the data to the df_answers DataFrame
        df_answers = pd.concat([df_answers, df], ignore_index=True)
        

    
    #if error continue
    
    #df_answers['profile_type'] = df_answers['profile_type'].apply(lambda x: x[0])
    
    try:
        df_answers['profile_type'] = df_answers['profile_type'].apply(lambda x: x[0])
    except IndexError as e:
        print(f"An IndexError occurred: {e}")
        pass  # continue execution even if an IndexError occurs
    except Exception as e:
        print(f"An error occurred: {e}")
        pass  # continue execution for any other exception
    
    
    # convert the score and profile_type columns to int and string
    df_answers['score'] = df_answers['score'].apply(lambda x: int(x[0]) if isinstance(x, np.ndarray) and len(x) > 0 and isinstance(x[0], (int, np.integer)) else int(x) if isinstance(x, (int, np.integer)) else str(x))
    df_answers['profile_type'] = df_answers['profile_type'].apply(lambda x: int(x[0]) if isinstance(x, np.ndarray) and len(x) > 0 and isinstance(x[0], (int, np.integer)) else int(x) if isinstance(x, (int, np.integer)) else str(x))
    df_answers['question_type'] = df_answers['question_type'].apply(lambda x: str(x[0]) if isinstance(x, np.ndarray) and len(x) > 0 and isinstance(x[0], (str)) else str(x) if isinstance(x, (str)) else str(x))
    
    #remove "[]" and " ' " from the profile type column
    df_answers['profile_type'] = df_answers['profile_type'].str.strip('[]').str.strip("'")
    
    
    ## get the names of the tables inside Grist
    subdomain = "docs"
    doc_id = "nSV5r7CLQCWzKqZCz7qBor"
    table_id = "Form3"
    url = f"https://{subdomain}.getgrist.com/api/docs/{doc_id}/tables"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        tables = response.json()
        
    else:
        print(f"Request failed with status code {response.status_code}")
    
    #create a function to add the answers to the st.session_state
    def add_answers_to_grist_table(df_answers, table_id):

        # Convert DataFrame to list of records
        records = [{"fields": {"nom":record["nom"],"prenom":record["prenom"],"question":record["question"],"reponse":record["reponse"],"mail":record["mail"],"score": record["score"], "profile_type": record["profile_type"]}} for record in df_answers.to_dict(orient='records')]
        
        # Prepare the request body
        data = {"records": records}
        docId = "nSV5r7CLQCWzKqZCz7qBor"
        tableId = table_id

        # Use the Grist API to add the new rows to the specified Grist table
        url = f"https://{subdomain}.getgrist.com/api/docs/{docId}/tables/{tableId}/records"
        
        
        
        response = requests.post(url, headers=headers, json=data)
        st.write(response.json())
        st.write(records)
        
    if st.button("Je valide", key=78):
        add_answers_to_grist_table(df_answers, st.session_state.table_id)
        #st.session_state.selected_data = df_answers
        #conn.update(worksheet="Gatherizer", data=df_answers)
        st.success("Bien reçu ! A bientôt <3")
    
    
    # Create a form to assess the level of expertise of each respondent
    st.header("Parlons de vous (et de data) :floppy_disk: ")
    
    
    #define what the unique questions are depending on the score for each profile
    df_analyst = grist_question_df[grist_question_df['profile_type'] == 'Data Analyst']
    df_scientist = grist_question_df[grist_question_df['profile_type'] == 'Data Scientist']
    df_dpo = grist_question_df[grist_question_df['profile_type'] == 'Data Protection Officer']
    
    
    
    ############### create a logic to display questionns based on previous response
    
    unique_questions = np.array([])
    
    if df_answers[df_answers['profile_type'] == 'Data Analyst']['score'].sum() >= 4:
        unique_questions = np.append(unique_questions, df_analyst[df_analyst['question_type'] == 'expertise'].question.unique())
    
    if df_answers[df_answers['profile_type'] == 'Data Scientist']['score'].sum() >= 4:
        unique_questions = np.append(unique_questions, df_scientist[df_scientist['question_type'] == 'expertise'].question.unique())
    
    if df_answers[df_answers['profile_type'] == 'Data Protection Officer']['score'].sum() >= 4:
        unique_questions = np.append(unique_questions, df_dpo[df_dpo['question_type'] == 'expertise'].question.unique())
    
    ################ end 
    
    ## for each question, display the question and the possible answers
    for i, question_people in enumerate(unique_questions):
        st.write(question_people)
        answer_people = st.selectbox("Votre réponse", grist_question_df[grist_question_df.question == question_people].reponse.unique(), index=None, key = i)
        question_type = grist_question_df[grist_question_df.reponse == answer_people].question_type.values
        score = grist_question_df[grist_question_df.reponse == answer_people].score.values
        profile_type_val = grist_question_df[grist_question_df.reponse == answer_people].profile_type.values
        df = pd.DataFrame({'nom': [nom], 'prenom': [prenom], 'mail': [mail],'question': [question_people],'question_type':[question_type], 'reponse': [answer_people],'score': [score],'profile_type':[profile_type_val]})
        
    
        # Append the data to the df_answers DataFrame
        df_answers = pd.concat([df_answers, df], ignore_index=True)
    
    # convert the score and profile_type columns to int and string
    df_answers['score'] = df_answers['score'].apply(lambda x: int(x[0]) if isinstance(x, np.ndarray) and len(x) > 0 and isinstance(x[0], (int, np.integer)) else int(x) if isinstance(x, (int, np.integer)) else str(x))
    df_answers['profile_type'] = df_answers['profile_type'].apply(lambda x: int(x[0]) if isinstance(x, np.ndarray) and len(x) > 0 and isinstance(x[0], (int, np.integer)) else int(x) if isinstance(x, (int, np.integer)) else str(x))
    df_answers['question_type'] = df_answers['question_type'].apply(lambda x: str(x[0]) if isinstance(x, np.ndarray) and len(x) > 0 and isinstance(x[0], (str)) else str(x) if isinstance(x, (str)) else str(x))

    #remove "[]" and " ' " from the profile type column
    df_answers['profile_type'] = df_answers['profile_type'].str.strip('[]').str.strip("'")
    
    
   ## get the names of the tables inside Grist
    subdomain = "docs"
    doc_id = "nSV5r7CLQCWzKqZCz7qBor"
    table_id = "Form3"
    url = f"https://{subdomain}.getgrist.com/api/docs/{doc_id}/tables"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        tables = response.json()
        
    else:
        print(f"Request failed with status code {response.status_code}")
    
    #create a function to add the answers to the st.session_state
    def add_answers_to_grist_table(df_answers, table_id):

        # Convert DataFrame to list of records
        records = [{"fields": {"nom":record["nom"],"prenom":record["prenom"],"question":record["question"],"reponse":record["reponse"],"mail":record["mail"],"score": record["score"], "profile_type": record["profile_type"],"question_type": record["question_type"]}} for record in df_answers.to_dict(orient='records')]
        
        # Prepare the request body
        data = {"records": records}
        docId = "nSV5r7CLQCWzKqZCz7qBor"
        tableId = table_id

        # Use the Grist API to add the new rows to the specified Grist table
        url = f"https://{subdomain}.getgrist.com/api/docs/{docId}/tables/{tableId}/records"
        
        
        response = requests.post(url, headers=headers, json=data)
        
    
    ## Create a button to add the answers to the Grist table
    if st.button("Je valide"):
        
        add_answers_to_grist_table(df_answers, st.session_state.table_id)
        st.session_state.selected_data = df_answers
        #conn.update(worksheet="Gatherizer", data=df_answers)
        st.success("Bien reçu ! A bientôt <3")
    
    
    st.header("Qu'en est-il de votre expertise (toujours data) :smile: ")
    
    
    #define what the unique questions are depending on the score for each profile
    df_analyst = grist_question_df[grist_question_df['profile_type'] == 'Data Analyst']
    df_scientist = grist_question_df[grist_question_df['profile_type'] == 'Data Scientist']
    df_dpo = grist_question_df[grist_question_df['profile_type'] == 'Data Protection Officer']
    
    ############### create a logic to display questionns based on previous response
    

    unique_questions_mastery = np.array([])

    score_analyst_df = df_answers[df_answers['profile_type'] == 'Data Analyst'] 
    score_scientist_df = df_answers[df_answers['profile_type'] == 'Data Scientist'] 
    score_dpo_df = df_answers[df_answers['profile_type'] == 'Data Protection Officer'] 

    
    
    for score_df in [score_analyst_df, score_scientist_df, score_dpo_df]:
        sum_expertise_score = score_df[score_df['question_type'] == 'expertise']['score'].sum()

        if sum_expertise_score > 6:
            if score_df is score_analyst_df:
                unique_questions_mastery = np.append(unique_questions_mastery, df_analyst[df_analyst['question_type'] == 'mastery'].question.unique())
            elif score_df is score_scientist_df:
                unique_questions_mastery = np.append(unique_questions_mastery, df_scientist[df_scientist['question_type'] == 'mastery'].question.unique())
            elif score_df is score_dpo_df:
                unique_questions_mastery = np.append(unique_questions_mastery, df_dpo[df_dpo['question_type'] == 'mastery'].question.unique())
    
    
    
    
    ################ end 
    
    ## for each question, display the question and the possible answers
    for i, question_people in enumerate(unique_questions_mastery):
        st.write(question_people)
        answer_people = st.selectbox("Votre réponse", grist_question_df[grist_question_df.question == question_people].reponse.unique(), index=None, key = i+104)
        score = grist_question_df[grist_question_df.reponse == answer_people].score.values
        profile_type_val = grist_question_df[grist_question_df.reponse == answer_people].profile_type.values
        df = pd.DataFrame({'nom': [nom], 'prenom': [prenom], 'mail': [mail],'question': [question_people], 'reponse': [answer_people],'score': [score],'profile_type':[profile_type_val]})
        
    
        # Append the data to the df_answers DataFrame
        df_answers = pd.concat([df_answers, df], ignore_index=True)
    
    # convert the score and profile_type columns to int and string
    df_answers['score'] = df_answers['score'].apply(lambda x: int(x[0]) if isinstance(x, np.ndarray) and len(x) > 0 and isinstance(x[0], (int, np.integer)) else int(x) if isinstance(x, (int, np.integer)) else str(x))
    df_answers['profile_type'] = df_answers['profile_type'].apply(lambda x: int(x[0]) if isinstance(x, np.ndarray) and len(x) > 0 and isinstance(x[0], (int, np.integer)) else int(x) if isinstance(x, (int, np.integer)) else str(x))
    #remove "[]" and " ' " from the profile type column
    df_answers['profile_type'] = df_answers['profile_type'].str.strip('[]').str.strip("'")
    
    
   ## get the names of the tables inside Grist
    subdomain = "docs"
    doc_id = "nSV5r7CLQCWzKqZCz7qBor"
    table_id = "Form3"
    url = f"https://{subdomain}.getgrist.com/api/docs/{doc_id}/tables"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        tables = response.json()
        
    else:
        print(f"Request failed with status code {response.status_code}")
    
    #create a function to add the answers to the st.session_state
    def add_answers_to_grist_table(df_answers, table_id):

        # Convert DataFrame to list of records
        records = [{"fields": {"nom":record["nom"],"prenom":record["prenom"],"question":record["question"],"reponse":record["reponse"],"mail":record["mail"],"score": record["score"], "profile_type": record["profile_type"]}} for record in df_answers.to_dict(orient='records')]
        
        # Prepare the request body
        data = {"records": records}
        docId = "nSV5r7CLQCWzKqZCz7qBor"
        tableId = table_id

        # Use the Grist API to add the new rows to the specified Grist table
        url = f"https://{subdomain}.getgrist.com/api/docs/{docId}/tables/{tableId}/records"
        
        
        response = requests.post(url, headers=headers, json=data)
        
        
    
    
    ## Create a button to add the answers to the Grist table
    if st.button("Je valide", key = 201):
        
        add_answers_to_grist_table(df_answers, st.session_state.table_id)
        st.session_state.selected_data = df_answers
        #conn.update(worksheet="Gatherizer", data=df_answers)
        st.success("Bien reçu ! A bientôt <3")
    
    
    # Now, outside the loop, you can display the complete df_answers DataFrame
    #st.dataframe(df_answers)
    
# Le vent souffla plus fort alors que le programmeur invoquait le puissant radar graph pour analyser la distribution des profils. 
# Des profils émergeaient, formant des constellations dans le ciel de données.

def dispenser_tab():
    
    
    ## Load Data from Grist
    subdomain = "docs"
    doc_id = "nSV5r7CLQCWzKqZCz7qBor"
    table_id = st.session_state.table_id
    print(table_id)
    url = f"https://{subdomain}.getgrist.com/api/docs/{doc_id}/tables/{table_id}/records"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print("Houra")
        columns = data['records'][0]['fields'].keys()
        #print(list(columns)[0])
        # Process the data as needed
    else:
        print(f"Request failed with status code {response.status_code}")
    
    #turn data into a dataframe with columns "nom","prenom","mail","question","answer","score","profile_type"
    records = data['records']
    data = pd.json_normalize(records, sep='_')
    data.columns = [col.replace('fields_', '') for col in data.columns]
    
    
    st.header("Position des profils")
    st.markdown("Grâce au _radar graph_, analysez la distribution des profils au sein de votre population")
    with elements("nivo_charts"):
        form_data = data
        #filter form data so to delete all rows where "nom" is empty
        # Assuming 'nom' is the column name where you want to check for empty values
        form_data_filtered = form_data[form_data['mail'].str.contains('@')]
        # Obtenez les valeurs uniques de la colonne "nom"
        unique_noms = form_data_filtered['nom'].unique()

        # Créez la structure de données DATA
        DATA = []

        # Pour chaque profil unique, créez un dictionnaire
        for profile_type in form_data_filtered['profile_type'].unique():
            profile_data = {"profile": profile_type}

            # Parcourez les noms uniques
            for nom in unique_noms:
                # Filtrer le DataFrame pour obtenir les lignes correspondant au nom et profil
                filtered_data = form_data_filtered[(form_data_filtered['nom'] == nom) & (form_data_filtered['profile_type'] == profile_type)]
        
                # Vérifiez s'il y a des données pour le nom et le profil actuels
                if not filtered_data.empty:
                    score = filtered_data['score'].tolist()
                    score = [int(x) for x in score if isinstance(x, (int, np.integer))]
                    total_score = sum(score)
                    profile_data[nom] = total_score
            
            DATA.append(profile_data)

            

        with mui.Box(sx={"height": 500}):
            nivo.Radar(
                data=DATA,
                keys=unique_noms,
                indexBy="profile",
                maxValue = 40,
                valueFormat=">-.2f",
                curve="linearClosed",
                margin={ "top": 70, "right": 80, "bottom": 40, "left": 80 },
                borderColor={ "theme": "grid.line.stroke" },
                gridLabelOffset=36,
                dotSize=8,
                dotColor={ "theme": "background" },
                dotBorderWidth=2,
                motionConfig="wobbly",
                legends=[
                    {
                        "anchor": "top-left",
                        "direction": "column",
                        "translateX": -50,
                        "translateY": -40,
                        "itemWidth": 80,
                        "itemHeight": 20,
                        "itemTextColor": "#999",
                        "symbolSize": 12,
                        "symbolShape": "circle",
                        "effects": [
                            {
                                "on": "hover",
                                "style": {
                                    "itemTextColor": "#000"
                                }
                            }
                        ]
                    }
                ],
                theme={
                    "background": "#FFFFFF",
                    "textColor": "#31333F",
                    "tooltip": {
                        "container": {
                            "background": "#FFFFFF",
                            "color": "#31333F",
                        }
                    }
                }
            )
# Mais la quête n'était pas terminée. Le héros se plongea dans la création des groupes, attribuant des profils à des cohortes spécifiques. 
# Le tableau se transforma en un champ de bataille stratégique, où chaque programmeur était assigné à sa place.

    #create a df that is form_data df but group by name
    #form_data = form_data[form_data['score'].notna()]
    #form_data['score'] = form_data['score'].astype(int)
    #form_data_grouped = form_data.groupby(['nom', 'prenom'])['score'].mean().reset_index()
    #form_data_grouped['groupe'] = pd.NA
    #st.header("Constitution des groupes")
    #st.markdown("Répartissez les profils au sein de groupes")
    #groups = st.data_editor(
    #    form_data_grouped,
    #    column_config={
    #        "group": st.column_config.NumberColumn(
    #            "Group",
    #            help="What group",
    #            min_value=1,
    #            max_value=10,
    #            step=1,
    #            format="%d 👭",
    #    )
    #    }
    #)
    #st.dataframe(groups)
    #st.write(st.session_state)
    #if st.button("Assigner", key=8):
    #    conn.update(worksheet="Dispenser", data=groups)
    #    st.success("C'est fait !")
        



# Create a function to display the selected tab content
def display_tab_content(tab_label):
    if tab_label == "Qualification":
        colorizer_tab()
    elif tab_label == "Recrutement":
        gatherizer_tab()
    elif tab_label == "Position":
        dispenser_tab()
#
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

# Get the id of the menu item clicked
#st.info(f"Selected tab: {selected_tab_label}")
#st.info(f"Menu {menu_id}")

# Et ainsi se termina cette saga épique, où le codeur du monde virtuel triompha des énigmes, manipula les données et forgea un chemin vers la victoire. 
# Un conte de programmation, où chaque ligne de code était une ligne de l'histoire, tissée dans le tissu du royaume virtuel.
