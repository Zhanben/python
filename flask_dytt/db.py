from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.types import Integer, String
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()
DB_CONNECT_STRING = 'mysql+pymysql://root:hillstone@localhost:3306/film?charset=utf8'
engine = create_engine(DB_CONNECT_STRING, echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,                                         bind=engine))
Base = declarative_base()

class Film(BaseModel):
    __tablename__ = 'film'
    uid = Column(Integer, primary_key=True)
    name_cn = Column(String(100))
    name = Column(String(50))
    year = Column(String(10))
    country = Column(String(30))
    category = Column(String(30))
    language = Column(String(20))
    subtitle = Column(String(20))
    release_date = Column(String(50))
    score = Column(String(30))
    file_size = Column(String(10))
    movie_duration = Column(String(20))
    director = Column(String(30))
    image_name = Column(String(50))
    download_url = Column(String(500))

def init_db():
    Base.metadata.create_all(bind=engine)