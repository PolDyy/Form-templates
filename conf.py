import os
from dotenv import load_dotenv

env_dir = os.getcwd()
env_file = os.path.join(env_dir, '.env')

load_dotenv(env_file)

# postgres
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

