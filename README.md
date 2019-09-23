# Lottery [demo](https://lottery-6-49.herokuapp.com/)

### Prerequisites
* Python 3.6.7

### Run the project

```
pip install -r requirements.txt
export DATABASE_URL=postgres://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}
python manage.py migrate
python manage.py runserver
```

## Run the tests
Run `pytest` command in the project root directory.
