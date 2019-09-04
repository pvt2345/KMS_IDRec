from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import config


host = config.DATABASE_CONFIG['host']
port = config.DATABASE_CONFIG['port']
user = config.DATABASE_CONFIG['user']
password = config.DATABASE_CONFIG['password']
dbname = config.DATABASE_CONFIG['dbname']

str_connection = 'mysql://' + user + ':' + password + '@' + host + ':' + str(port) + '/' + dbname + '?charset=utf8'
engine = create_engine(str_connection, echo=False)

connection = engine.connect()
Session = sessionmaker(bind=engine)

Base = declarative_base()