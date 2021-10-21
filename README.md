# Locations API

French locations API

Next steps : 
- Docker
- Angular home page

Access [API](http://127.0.0.1:8000/locations/regions)  

Access [API with json format](http://127.0.0.1:8000/locations/regions/?format=json)   

## Install and init postgreSQL

To install and init postgreSQL :

``` 
    sudo apt-get install postgresql-12 
    sudo -i -u postgres
    psql
    CREATE ROLE basic_user LOGIN SUPERUSER PASSWORD 'basic_pwd';
    CREATE DATABASE basic_db OWNER basic_user;
    \q
    exit
```

## Install python and pipenv
```
sudo apt install python3.8
sudo apt install pipenv
```

## Init project 

To initialise the project from main directory :

```
    source ./run.sh init_project
```

Packages are : 
 - Django 
 - psycopg2 
 - djangorestframework 
 - pandas 
 - requests 
 - django-extensions

## Run venv

To run venv from main directory : 

```
    source ./run.sh run_venv
```

To exit venv : 

```
    exit
```

## Import data

To import data from main directory : 

```
    ./run.sh import_data
```

## OSM data

To create or update osm_data.csv  from main directory : 

```
    ./run.sh osm_data
```
## Run django server 

To run the server from main directory : 

```
    ./run.sh run_server
```

## Data Base infos :

data base : basic_db  
user : basic_user  
password : basic_pwd  
