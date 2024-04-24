# Data Position Studio

Le Data Position Studio permet de générer des Data Position. 

Un Data Position est un outil qui permet à la fois : 
* aux individus de savoir à quel(s) profil(s) data ils peuvent être affiliés (Data Analyst, Data Scientist, etc.)
* aux organisations de mieux comprendre leur patrimoine d'expertise data

## Pourquoi un Data Position Studio ? 

En 2024, les frontières des différents métiers de la donnée sont encore floues et leurs définitions varient d'une organisation à une autre. Dans ce cadre, il est opportun de permettre aux organisations de créer leur propre système de qualification des profils et de proposer une infrastructure légère pour déployer leur Data Position spécifique. Le Data Position Studio répond à ce besoin. 

Aussi, le Data Position Studio a vocation à devenir un outil communautaire qui recense tous les Data Position créés **de manière à ce qu'ils puissent être réutilisés.** 

## Documentation technique 

Le Data Position Studio est constitué : 
* D'un `document` Grist dans lequel sont stockées des `tables` de données brutes. Chaque table correspond à un Data Position créé par la communauté. On trouve aussi dans ce document une `table` de configuration.
* D'un `repository` Github qui héberge le code source (écrit en Python) du Data Position Studio
* D'une `application` Streamlit qui exectue le code Python

![tech_stack_data_position](https://github.com/ArthurSrz/data-position-studio/assets/55806298/4d7585ba-961c-46c7-8b1b-5480eea330d8)


### Les tables de données brutes. 

Chaque table de données brutes permet de stocker tous les éléments qui constituent un Data Position, à savoir : 
* une liste de profils data 
* un ensemble de questions/réponses permettant d'identifier un profil data
* un score associé à chaque réponse permettant de préciser le niveau d'expertise du répondant sur les différents profils data 

#### Schema

Voir [Table Schema](Schema_table.json)

### Le code source

Les fichiers clés :

```
data-position-studio/
├── pages/
│   ├── Recrutement.py
│   └── Position.py
└── Hello.py
```
### Maintenance 

#### Pour ajouter de nouveaux Data Position créés par la communauté 

##### 1. Créer une table de donnée brute dans le document Grist central 
Cette table de donnée doit être en conformité avec le schéma décrit dans le [Table Schema](Schema_table.json). Pensez à bien noter le `Table_id` de la table. 

##### 2. Modifier le code source
Pour ajouter les Data Position créés par la communauté, il faut se rendre dans le fichiers `Hello.py` et ajouter sous la ligne 96 le bout de code suivant en adaptant `table_id{x}`, `data{x}` et `{grist_table_id{x}}` : 

```
## Load Data Position {X}
subdomain = "docs"
doc_id = "nSV5r7CLQCWzKqZCz7qBor"
table_id_{x} = {grist_table_id{x}}
url = f"https://{subdomain}.getgrist.com/api/docs/{doc_id}/tables/{table_id_{x}}/records"
response = requests.get(url, headers=headers)
if response.status_code == 200:
    data{x} = response.json()
    columns = data{x}['records'][0]['fields'].keys()
    # Process the data as needed
else:
    print(f"Request failed with status code {response.status_code}")
```

Egalement ajouter un nouveau `st.container` sous la ligne 166 et y insérer le code suivant en adaptant la `liste de profils` avec les profils présents au sein du Data Position et `table_id_{x}`

```
st.text("Data Position Maitre")
expander = st.expander("Description")
expander.write("Le Data Position par défaut créé par Datactivist")
#make checkboxes where the users get to choose which profile he is going to evaluate
profiles = st.multiselect("Choix des profils",[liste_de_profils],max_selections=20)      
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
                
                
                
    df_config = pd.DataFrame({'table_id': table_id_{x}, 'profiles': [profiles]})
    #st.dataframe(df_config)
    #send data to the config grist
    add_config(df_config)
    st.success("Data position chargé 🚚")
```

#### Pour déployer un Data Position spécifique

##### 1. Dupliquer le document central Grist sur le compte du client
Penser à bien noter la clé API du document
##### 2. Forker le repo Github sur le compte du client
##### 3. Créer/Utiliser un compte Streamlit Cloud pour le client
Avec ce compte Streamlit cloud, créer une application reliée au repo qui vient d'être créé. 
Dans les réglages de l'application --> Secrets ajoutez les éléments suivants

```
grist_api_key = "{clé_api_du_document_grist}"

[passwords]
# Follow the rule: username = "password"
username = "password"
```
