if [ ! -d  ]; then
        git clone git@github.com:CS428-Group5/cs428-backend.git
        cd 
        python3 -m venv .env
        source .env/bin/activate
        pip install -r requirements.txt
        python3 manage.py migrate
        python3 manage.py runserver
    else
        cd 
        git pull origin master
    fi
