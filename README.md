# Store Server

The project for study Django.

#### Stack:

- [Python](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/)
- [Redis](https://redis.io/)

## Local Developing

All actions should be executed from the source directory of the project and only after installing all requirements.

1. Firstly, create and activate a new virtual environment:
 
   
2. Install packages:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
   
3. Run project dependencies, migrations, fill the database with the fixture data etc.:
   ```bash
   python manage.py migrate
   python manage.py loaddata <path_to_fixture_files>
   python manage.py runserver 
   ```
   
4. Run [Redis Server](https://redis.io/docs/getting-started/installation/):
   ```bash
   redis-server
   ```
   
5. Add and run Celery:
   ```bash
   celery -A store worker --loglevel=INFO
   ```
