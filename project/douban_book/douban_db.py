from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from password import PASSWORD

# 基础类
Base = declarative_base()

engine = create_engine(
    'mysql+pymysql://root:{}@127.0.0.1:3306/py_crawl?charset=utf8'.format(PASSWORD),
    echo=True
)


class Book(Base):
    __tablename__ = 'book'
    id = Column('id', Integer(), primary_key=True, autoincrement=True)
    title = Column('title', String(20))
    info = Column('info', String(50))
    star = Column('star', String(10))
    pl = Column('pl', String(20))
    introduce = Column('introduce', Text())


Base.metadata.create_all(engine)

session = sessionmaker(engine)
sess = session()