from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

sqleng = create_engine("sqlite:///database/log.db", echo=True)
sqlbase = declarative_base()

class User(sqlbase):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

    def __init__(self, username, password):
        self.username = username
        self.password = password

class Convo(sqlbase):
    __tablename__ = "convos"
    id = Column(Integer, primary_key=True)
    convoid = Column(String)
    chatmsg = Column(String)
    timestamp = Column(String)
    username = Column(String)

    def __init__(self, convoid, chatmsg, timestamp, username):
        self.convoid = convoid
        self.chatmsg = chatmsg
        self.timestamp = timestamp
        self.username = username

class Loggedon(sqlbase):
    __tablename__ = "loggedons"
    date = Column(String)
    msg = Column(String)
    id = Column(Integer, primary_key=True)

    def __init__(self, date, msg):
        self.date = date
        self.msg = msg

sqlbase.metadata.create_all(sqleng)
