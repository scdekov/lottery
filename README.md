# Lottery [demo](https://lottery-6-49.herokuapp.com/)
*Note: for test purposes games are not reset between every draw so all tickets go in single draw and draw can be performed for the only game multiple times*

### Prerequisites
* Python 3.6.7
* PostgresDB 9+

### Run the project

```
pip install -r requirements.txt
export DATABASE_URL=postgres://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}
python manage.py migrate
python manage.py runserver
```

## Run the tests
Run `pytest` command in the project root directory.
