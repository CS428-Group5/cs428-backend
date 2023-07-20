gcloud compute ssh instance-1 -- command "echo 'if [ ! -d cs428-backend ]; then
        git clone git@github.com:CS428-Group5/cs428-backend.git
        cd cs428-backend
        python3 -m venv .env
        source .env/bin/activate
        pip install -r requirements.txt
        python3 manage.py migrate
        python3 manage.py runserver
    else
        cd cs428-backend
        git pull origin master
    fi' > init_script.sh"