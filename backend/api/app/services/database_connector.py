import os
import psycopg2
import logging as logging
from dotenv import load_dotenv


log = logging.getLogger(__name__)

def get_database_connection():
    load_dotenv(dotenv_path='../.env')
    try:
        print(os.getenv("POSTGRES_HOST"))
        with psycopg2.connect(
            database="mydatabase",
            host="database",
            user="myuser",
            password="mypassword",
            port="5432"
        ) as conn:
            return conn
    except Exception as e:
        print(e)
        log.error('Error while connecting to database')
        raise e