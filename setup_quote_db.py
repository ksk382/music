from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
import socket
from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table
from sqlalchemy.orm import sessionmaker, scoped_session


db = declarative_base()

class quote(db):
    __tablename__='quote'

    id = Column(Integer, primary_key=True)
    line = Column(String(64), index=True)
    speaker = Column(String(64), index=True)
    source = Column(String(64), index=True)

    def __repr__(self):
        return self.id, self.line, self.speaker, self.source

class quote2(db):
    __tablename__='quote2'

    id = Column(Integer, primary_key=True)
    line = Column(String(64), index=True)
    speaker = Column(String(64), index=True)
    source = Column(String(64), index=True)
    #add a column for whether the quote has been used before
    use_count = Column(Integer, index=True)
    last_used = Column(String(64), index=True)

    def __repr__(self):
        return self.id, self.line, self.speaker, self.source

def make_new_db():
    # creation of the SQL database and the "session" object that is used to manage
    # communications with the database
    engine = create_engine('sqlite:///dbQuotes2.db')
    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)
    metadata = MetaData(db)
    db.metadata.create_all(engine)
    print('dbQuotes2.db created')
    return

if __name__ == "__main__":
    print(quote.__table__)



