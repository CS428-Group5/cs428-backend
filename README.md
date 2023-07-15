# CS428-backend


## Run Django server
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Use Django admin page
- Create a superuser with
```
python manage.py createsuperuser
```
- Go to **[Admin page](http://127.0.0.1:8000/admin)**
- User the superuser to login into admin page

## Use Swagger API to see and use API
- Go to **[Swagger API](http://127.0.0.1:8000/api/docs)**