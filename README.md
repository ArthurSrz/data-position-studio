# La forge à Data Position

L'architecture est constituée : 

- d'une **base de données** qui va permettre de stocker : 

	- les critères qui vont permettre de qualifier les profils
	- les réponses de la population aux questions qui permettent de collecter les données relatives aux critères 
	- les groupes dans lesquels les membres de la population sont répartis

* d'une **application web** qui permettra au concepteur du Data Position de : 

	* créer une table de qualification des membres de la population 
	* recruter et qualifier des membres de la population via un questionnaire
	* analyser la position de tous les membres de la population et les répartir en différents groupes 

## A propos de la base de données

<p><span style="color: red;"><b>Attention</b> : 1 Data position = 1 base de données.</span> Il faudra donc demander la création d'une base de données à Datactivist pour pouvoir créer la base </p>

Il s'agit d'un Google sheet avec 3 onglets : 

### L'onglet "Colorizer" 
Il correspond à la Table de qualification et va permettre de stocker : 
	- les types de profils *data* que le concepteur veut pouvoir évaluer dans la population choisie
	- les questions posées par le concepteur du dataposition pour identifier les différentes profils *data* au sein de sa population
	- les réponses possibles pour chaque question
	- le niveau de maitrise associé à chacune des réponses 


![](media/onglet_colorizer.png)
<center>Aperçu de l'onglet "Colorizer"</center>


### L'onglet "Gatherizer" 
Il stocke les réponses des membres de la population aux questions qui permettent de qualifier les profils

![](media/onglet_gatherizer.png)
<center>Aperçu de l'onglet "Gatherizer"</center>


### L'onglet "Dispenser" 
Il stocke la répartition des membres de la population en différents groupes

![](media/onglet_dispenser.png)
<center>Aperçu de l'onglet "Dispenser"</center>

## A propos de l'application Web 

L'application Web permet d'accéder via une seule URL à toutes les fonctionnalités du Data position. Ainsi, le concepteur pourra y : 

### Créer sa table de qualification

![](media/onglet_table_qualification.png)
<center>Aperçu de l'onglet "Qualification"</center>


### Diffuser le questionnaire nécessaires pour qualifier les membres de sa population

![](media/onglet_recensement.png)
<center>Aperçu de l'onglet "Recrutement"</center>

### Visualiser, en fonction des réponses, la répartition par profil des membres de sa population 

![](media/onglet_position.png)
<center>Aperçu de l'onglet "Recrutement"</center>

### Dispatcher dans différents groupes les membres de sa population . 

