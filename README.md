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

Pour ajouter les Data Position créés par la communauté, il faut se rendre dans le fichiers `Hello.py` et ajouter sous la ligne 96 le bout de code suivant en adaptant `table_id{x}` et `data{x}` : 

```
## Load Data Position {X}
subdomain = "docs"
doc_id = "nSV5r7CLQCWzKqZCz7qBor"
table_id_{x} = {grist_table_id}
url = f"https://{subdomain}.getgrist.com/api/docs/{doc_id}/tables/{table_id_{x}}/records"
response = requests.get(url, headers=headers)
if response.status_code == 200:
    data{x} = response.json()
    columns = data{x}['records'][0]['fields'].keys()
    # Process the data as needed
else:
    print(f"Request failed with status code {response.status_code}")
```




