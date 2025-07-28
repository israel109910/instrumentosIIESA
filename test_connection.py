import os
import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv

load_dotenv()  # Carga variables del archivo .env

DATABASE_URL = os.getenv('DATABASE_URL')

try:
    conn = psycopg2.connect(DATABASE_URL)
    print("Conexión exitosa a la base de datos.")
    conn.close()
except OperationalError as e:
    print("Error de conexión:", e)
