from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

user_name = "ssafy"
user_password = "ssafy"
db_host = "127.0.0.1"
db_name = "testssak3"


SQLALCHEMY_DATABASE_URL = 'mysql://%s:%s@%s/%s?charset=utf8' % (
    user_name,
    user_password,
    db_host,
    db_name
)

ENGINE = create_engine(
    SQLALCHEMY_DATABASE_URL,
    encodings = "utf-8",
    echo = True
)

session = sessionmaker(autocommit=False,
                       autoflush=False,
                       bind=ENGINE)

Base = declarative_base()