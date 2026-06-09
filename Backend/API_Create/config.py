from dotenv import load_dotenv
import os

load_dotenv()

class Config:

    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = int(os.getenv("DB_PORT")==None)
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")

    KAFKA_SERVER = os.getenv("KAFKA_SERVER")