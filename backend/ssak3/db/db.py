from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

user_name = "ssafy101"
user_password = "ssafy101"
db_host = "j9b201.p.ssafy.io"
db_name = "ssak3"


DATABASE_URL = 'mysql+pymysql://%s:%s@%s/%s?charset=utf8' % (
    user_name,
    user_password,
    db_host,
    db_name
)

ENGINE = create_engine(
    DATABASE_URL,
    echo=True
)

session = sessionmaker(autocommit=False,
                       autoflush=False,
                       bind=ENGINE)

Base = declarative_base()