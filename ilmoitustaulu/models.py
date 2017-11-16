from sqlalchemy import Column, Integer, String, Boolean,ForeignKey
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
    image = Column(String(255), unique=False)
    user =  Column(Integer, ForeignKey(User.id), nullable=False)
    price = Column(String(25), unique=False)
    location = Column(String(55), unique=False)
    urlid = Column(String(50), unique=True)
    category = Column(String(50), unique=False)
    
    #user_Id = relationship('User', foreign_keys='Event.user')

    
    def __init__(self, name=None, description=None, user=None, price=None, location=None, image=None, category=None):
        self.name = name
        self.description = description
        self.user = user
        self.price = price
        self.location = location
        self.image = image
        self.category = category
        self.urlid = name + '_%s' % str(time.time()).replace(".", "") 
    #ei pakollinen    
    #def __repr__(self):
     #   return '<Event %r>' % (self.name)

     
class UserSavedEvents(Base):
    __tablename__='usersavedevents'
    id = Column(Integer, primary_key = True)
    user = Column(Integer, ForeignKey(User.id), unique=False)
    event = Column(Integer, ForeignKey(Event.id), unique=False)
    
    def __init__(self, user=None, event=None):
        self.user=user
        self.event=event

