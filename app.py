from flask import Flask
from flask_restful import Api
from database import db
from resources import EmployeeResource, PDFGenerationResource
from models import Employee

app = Flask(__name__)
api = Api(app)


api.add_resource(EmployeeResource, '/employees', '/employees/<int:employee_id>')
api.add_resource(PDFGenerationResource, '/generate-pdf/<int:employee_id>')

if __name__ == '__main__':
    db.connect()
    db.create_tables([Employee])
    app.run(debug=True)
