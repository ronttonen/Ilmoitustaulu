from sqlalchemy import Column, Integer, String, Boolean
from ilmoitustaulu.database import Base
from flask_login import UserMixin


class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    password = Column(String(50), unique=False)
    

    def __init__(self, name=None, email=None, password=None):
        self.name = name
        self.email = email
        self.password = password
        
  
    
        
    #ei pakollinen
    #def __repr__(self):
     #   return '<User %r>' % (self.name)
    
class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=False)
    urlid = Column(String(50), unique=True)
    
    def __init__(self, name=None, urlid=None):
        self.name = name
        self.urlid = name + '_ %s' % (Event.query.count()+1) 
    
    #ei pakollinen    
    #def __repr__(self):
     #   return '<Event %r>' % (self.name)