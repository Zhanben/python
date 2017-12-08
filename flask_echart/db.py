from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.types import CHAR, Integer,DateTime, Float
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()
DB_CONNECT_STRING = 'mysql+pymysql://root:hillstone@localhost:3306/app?charset=utf8'
engine = create_engine(DB_CONNECT_STRING, convert_unicode=True, echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    Base.metadata.create_all(bind=engine)


class Cpu(BaseModel):
    __tablename__ = 'cpu_moniter'
    id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(DateTime, nullable=False)
    cpu1 = Column(Float(precision=2), nullable=False)
    cpu2 = Column(Float(precision=2), nullable=False)
    cpu3 = Column(Float(precision=2), nullable=False)
    cpu4 = Column(Float(precision=2), nullable=False)
