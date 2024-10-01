# flask-with-celery


Command to run celery server for windows :
<br>
(Use any one)
```
celery -A app_name worker -l info -P eventlet
celery -A app_name worker --pool=solo -l info
celery -A main.celery_app worker --pool=solo -l info (In our case)
```

Command to run celery server for linux :
<br>
```
celery -A app_name worker -l info
```

# Creating virtual environment Linux

```
virtualenv venv --python=python3
source venv/bin/activate
pip install -r requirements.txt
```

# Creating virtual environment Windows

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
