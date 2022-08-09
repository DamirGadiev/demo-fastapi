import os

from decouple import config

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


class Config:
    PG_USERNAME = config('PG_USERNAME')
    PG_PASSWORD = config('PG_PASSWORD')
    PG_DATABASE = config('PG_DATABASE')
    PG_HOST=config('PG_HOST')
    SQLALCHEMY_DATABASE_URL = f"postgresql://{PG_USERNAME}:{PG_PASSWORD}@{PG_HOST}:5432/{PG_DATABASE}"
