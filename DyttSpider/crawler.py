from utils import *
from models import init_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


if __name__ == "__main__":
    DB_CONNECT_STRING = 'mysql+pymysql://root:hillstone@localhost:3306/film?charset=utf8'
    engine = create_engine(DB_CONNECT_STRING, echo=True)
    init_db(engine)
    DB_Session = sessionmaker(bind=engine)
    session = DB_Session()
    url = "http://www.dy2018.com/i/98729.html"
    response = do_request(url)
    film = extract_details1(response, url)

    session.add(film)
    session.commit()
