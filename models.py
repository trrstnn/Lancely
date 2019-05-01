import datetime
from datetime import date
from datetime import time
from datetime import datetime, timedelta
from wtforms import SelectField


#import everything from peewee because we might need it 
from peewee import *
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash

DATABASE = SqliteDatabase('lancely.db')

class User(UserMixin, Model):
    __table_args__ = {'extend_existing': True} 
    
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    name = CharField()
    location = CharField()
    lng = DoubleField(null=True)
    lat = DoubleField(null=True)
    password = CharField(max_length=100)
    experience = IntegerField(null=True)
    rate = IntegerField(null=True)
    summary = CharField(null=True)
    skills = CharField(max_length=100, null=True)
    category = CharField(null=True) 
    freelancer = BooleanField(index=True, default=False)
    joined_at = DateTimeField(default=date.today().strftime("%Y-%m-%d"))
    class Meta:
        
        database = DATABASE
        order_by = ('-timestamp',)
    
    #  function that creates a new user
    @classmethod
    def create_user(cls, username, email , password, name, freelancer,location):
        try:
    
            cls.create(
                username = username,
                email = email,
                password = generate_password_hash(password),
                name = name,
                freelancer = freelancer,
                location = location
            )
        except IntegrityError:
            raise ValueError("User already exists")

class Reviews(Model):
    user = ForeignKeyField(User, backref="Reviews")
    title = CharField()
    rating = IntegerField()
    content = CharField()
    timestamp = DateTimeField(default=datetime.now().strftime("%Y-%m-%d %H:%M"))

    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)

def initialize():
   DATABASE.connect()
   DATABASE.create_tables([User], safe=True)
   DATABASE.close()
