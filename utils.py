from models import Employee
from peewee import DoesNotExist

def check_email_exist(email):
    try:
        Employee.get(Employee.email == email)
        return True
    except DoesNotExist:
        return False
