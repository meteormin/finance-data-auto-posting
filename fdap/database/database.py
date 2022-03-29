from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, session
from sqlalchemy.ext.declarative import declarative_base
from fdap.config.config import Config

config = Config.DATABASE['mysql']

access_info = 'mysql://{id}:{passwd}@{host}/{db}?charset=utf8'.format(id=config['id'], passwd=config['password'],
                                                                      host=config['host'], db=config['db'])

engine = create_engine(access_info, convert_unicode=False)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    Base.metadata.create_all(engine)
