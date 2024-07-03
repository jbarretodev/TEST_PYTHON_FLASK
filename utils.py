from models import Employee

def check_email_exist(email):
  return Employee.get(Employee.email == email)