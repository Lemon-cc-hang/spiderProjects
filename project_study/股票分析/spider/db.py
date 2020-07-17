# 创建数据库
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
import PASSWORD

BASE = declarative_base()
engine = create_engine(
    "mysql+pymysql://root:{}@127.0.0.1:3306/test?charset=utf8".format(PASSWORD.PASSWORD),
    max_overflow=1500,   # 超过连接池大小外最多可以创建的链接
    pool_size=1500,  # 连接池大小
    echo=False,     # 调试信息展示
)


class StockData(BASE):
    __tablename__ = 'stock_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(125))
    date = Column(String(125))
    open = Column(String(125))
    high = Column(String(125))
    low = Column(String(125))
    close = Column(String(125))

# BASE.metadata.drop_all(engine)
BASE.metadata.create_all(engine)
Session = sessionmaker(engine)
sess = scoped_session(Session)