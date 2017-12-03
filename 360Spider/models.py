from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.types import CHAR, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()


class App360(BaseModel):
    __tablename__ = 'app360'
    id = Column(Integer, primary_key=True, autoincrement=True)
    soft_id = Column(Integer, unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    author = Column(String(50), nullable=False)
    download_num = Column(String(50), nullable=False)
    score = Column(Float, nullable=False)
    # comments_num = Column(Integer, nullable=False)
    update_time = Column(DateTime, nullable=False)
    version = Column(String(50))


class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args)
        return cls._instance


class DbManager(Singleton):
    def __init__(self, Dbstring):
        self.engine = create_engine(Dbstring, echo=True)
        self._dbSession = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
        )

    def init_db(self):
        BaseModel.metadata.create_all(self.engine)

    def closeDB(self):
        self._dbSession().close()

    def getAppWithSoftId(self, soft_id):
        db_item = self._dbSession.query(App360).filter(App360.soft_id == soft_id).first()
        if db_item:
            return db_item
        else:
            return None

    def saveAppItem(self, app_object):
        db_item = self._dbSession.query(App360).filter(App360.soft_id == app_object.soft_id).first()
        if not db_item:
            print("***************%s not in ****************************" % app_object.name)
            self._dbSession().add(app_object)
            self._dbSession().commit()


if __name__ == "__main__":
    DB_CONNECT_STRING = 'mysql+pymysql://root:hillstone@localhost:3306/app?charset=utf8'
    db = DbManager(Dbstring=DB_CONNECT_STRING)
    db.init_db()
