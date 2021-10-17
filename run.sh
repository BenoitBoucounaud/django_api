#!/bin/bash

function nicecho {
        # https://stackoverflow.com/questions/5947742/how-to-change-the-output-color-of-echo-in-linux
        LB='\033[1;34m' # Light Blue
        LP='\033[1;35m' # Light Purple
        LC='\033[1;36m' # Light Cyan
        ER='\033[0;33m' # Brown/Orange
        NC='\033[0m' # No Color
        case $1 in
                strong)
                        printf "\033[1;36m%s\033[0m\n" "$2" # Light Cyan
                        ;;
                blue)
                        printf "\033[1;34m%s\033[0m\n" "$2" # Light Blue
                        ;;
                error)
                        printf "\033[0;33m%s\033[0m\n" "$2" # Brown/Orange
                        ;;
                normal|*)
                        printf "\033[1;35m%s\033[0m\n" "$2" # Light Purple
                        ;;
        esac
}


function error_stop {
        nicecho "error" " <!> Error, stopping scripts <!>"
        exit 1
}


function init_project {
    nicecho "error" "** To init the project you need to type 'source ./run.sh init' **"
    nicecho "strong" "** Init pipenv **"
    pipenv --three
    nicecho "strong" "** Install packages **"
    pipenv install Django psycopg2 djangorestframework pandas requests django-extensions
    pipenv run ./backend/manage.py makemigrations
    pipenv run ./backend/manage.py migrate
}

function import_data {
    nicecho "strong" "** Import data **"
    pipenv run python ./backend/manage.py runscript imports 
}

function run_venv {
    nicecho "error" "** To run venv you need to type 'source ./run.sh run_venv' **"
    nicecho "strong" "** Running venv **"
    nicecho "noraml" "** Type deactivate to close venv **"
    pipenv shell
}


function run_server {
    nicecho "strong" "** Running server **"
    pipenv run python ./backend/manage.py runserver
}

function django_check {
    # check project's conformity
    nicecho "strong" "** Django check **"
    pipenv run python ./backend/manage.py check
}

function usage {
        echo "Usage: $0 <ACTION>"
        echo "Parameters :"
        echo " - ACTION values :"
        echo "   * init_project                        - Initiate project."
        echo "   * run_venv                            - Launching virtual environment."
        echo "   * import_data                         - Import data."
        echo "   * run_server                          - Launching Django server."
        echo "   * django_check                        - Check project's conformity."
}

# Checking parameters
if [[ "$1" == "" ]]; then
   echo "Missing arguments."
   usage
   exit 1
fi

case "$1" in
    init_project)
        init_project
        ;;
    run_venv)
        run_venv
        ;;
    import_data)
        import_data
        ;;      
    run_server)
        run_server
        ;;    
    django_check)
        django_check
        ;;  
    *)
        echo "Unvalid environment detected (${1})"
        usage
        exit 1
        ;;
esac
