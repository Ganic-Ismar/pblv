import os
import psycopg2
import logging as logging
from dotenv import load_dotenv


log = logging.getLogger(__name__)

def get_database_connection():
    load_dotenv(dotenv_path='../.env')
    try:
        with psycopg2.connect(
            database=os.getenv("POSTGRES_DB"),
            host=os.getenv("POSTGRES_HOST"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            port=os.getenv("POSTGRES_PORT")
        ) as conn:
            return conn
    except Exception as e:
        print(e)
        log.error('Error while connecting to database')
        raise e