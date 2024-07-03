from peewee import Model, CharField
from database import db

class Employee(Model):
    name = CharField()
    department = CharField()
    email = CharField()

    class Meta:
        database = db
