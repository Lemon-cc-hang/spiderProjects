from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from password import PASSWORD

BASE = declarative_base()
engine = create_engine(
    "mysql+pymysql://root:{}@127.0.0.1:3306/py_crawl?charset=utf8".format(PASSWORD),
    max_overflow=1500,   # 超过连接池大小外最多可以创建的链接
    pool_size=1500,  # 连接池大小
    echo=False,     # 调试信息展示
)

class House(BASE):
    __tablename__ = 'houses'
    id = Column(Integer, primary_key=True, autoincrement=True)
    block = Column(String(125))
    rent = Column(String(125))
    title = Column(String(125))
    data = Column(Text())


# BASE.metadata.drop_all(engine)
BASE.metadata.create_all(engine)
Session = sessionmaker(engine)
sess = scoped_session(Session)