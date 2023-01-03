from decouple import config


class Config:
    IS_AZURE_ENVIRONMENT = config("IS_AZURE_ENVIRONMENT")
    PG_USERNAME = config("PG_USERNAME")
    PG_PASSWORD = config("PG_PASSWORD")
    PG_DATABASE = config("PG_DATABASE")
    PG_HOST = config("PG_HOST")
    SQLALCHEMY_DATABASE_URL = (
        f"postgresql://{PG_USERNAME}:{PG_PASSWORD}@{PG_HOST}:5432/{PG_DATABASE}"
    )
