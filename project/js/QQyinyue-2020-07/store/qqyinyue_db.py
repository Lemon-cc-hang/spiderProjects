from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from password import PASSWORD

engine = create_engine(
	'mysql+pymysql://root:{}@localhost:3306/py_crawl?charset=utf8'.format(PASSWORD),
	max_overflow=500,   # 超过连接池大小外最多可以创建的链接
	pool_size=100,  # 连接池大小
	echo=False, # 调试信息展示
)
Base = declarative_base()


class Song(Base):
	__tablename__ = 'songs'
	song_id = Column(Integer, primary_key=True, autoincrement=True)
	song_name = Column(String(64))
	song_ablum = Column(String(64))
	song_mid = Column(String(50))
	song_singer = Column(String(50))


# 销毁数据库
# Base.metadata.drop_all(engine)
# 创建数据库
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
SQLSession = scoped_session(DBSession)