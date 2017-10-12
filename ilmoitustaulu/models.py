from sqlalchemy import Column, Integer, String, Boolean
from ilmoitustaulu.database import Base
from flask_login import UserMixin
import time
import hashlib, uuid

class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    password = Column(String(255), unique=False)
    salt = Column(String(255), unique=False)
    

    def __init__(self, name=None, email=None, password=None):
        self.name = name
        self.email = email
        salt = uuid.uuid4().hex
        hashed_password = hashlib.sha512(password + salt).hexdigest()
        self.salt = salt
        self.password = hashed_password
        

    
        
    #ei pakollinen
    #def __repr__(self):
     #   return '<User %r>' % (self.name)
    
class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=False)
    description = Column(String(255), unique=False)
    urlid = Column(String(50), unique=True)
    
    def __init__(self, name=None, urlid=None,description=None):
        self.name = name

        self.urlid = name + '_%s' % str(time.time()).replace(".", "") 
    #ei pakollinen    
    #def __repr__(self):
     #   return '<Event %r>' % (self.name)