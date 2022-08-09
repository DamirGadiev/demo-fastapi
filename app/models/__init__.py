import databases
import sqlalchemy

from config import Config

engine = sqlalchemy.create_engine(
    Config.SQLALCHEMY_DATABASE_URL, connect_args={}
)
metadata = sqlalchemy.MetaData()

database = databases.Database(Config.SQLALCHEMY_DATABASE_URL)
