from flask import request, send_file, jsonify
from flask_restful import Resource
from models import Employee
from schemas import Employee_Schema
import pdfkit
import io
import json
from utils import check_email_exist

employee_schema = Employee_Schema()
class EmployeeResource(Resource):
    def get(self, employee_id=None):
        if employee_id:
            try:
                employee = Employee.get(Employee.id == employee_id)
                return jsonify({
                    'id': employee.id,
                    'name': employee.name,
                    'department': employee.department,
                    'email': employee.email
                })
            except Employee.DoesNotExist:
                return {'error': 'Employee not found'}, 404
        else:
            employees = Employee.select()
            return jsonify([
                {'id': emp.id, 'name': emp.name, 'department': emp.department, 'email': emp.email}
                for emp in employees
            ])

    def post(self):
        data = request.get_json()
        
        errors = employee_schema.validate(data)
        
        if errors:
            return {'errors': errors}, 400
        
        if check_email_exist(data['email']):
            return {'error': 'Email already exists'}, 400
        
        employee = Employee.create(name=data['name'], department=data['department'], email=data['email'])
        
        employee_data = {
            'id': employee.id,
            'name': employee.name,
            'department': employee.department,
            'email': employee.email
        }
        
        json_data = json.dumps(employee_data)
        
        return json_data, 201

    def put(self, employee_id):
        try:
            employee = Employee.get(Employee.id == employee_id)
        except Employee.DoesNotExist:
            return {'error': 'Employee not found'}, 404
        data = request.get_json()
        employee.name = data.get('name', employee.name)
        employee.department = data.get('department', employee.department)
        employee.email = data.get('email', employee.email)
        
        employee.save()
        
        return jsonify({
            'id': employee.id,
            'name': employee.name,
            'department': employee.department,
            'email': employee.email
        })

    def delete(self, employee_id):
        try:
            employee = Employee.get(Employee.id == employee_id)
        except Employee.DoesNotExist:
            return {'error': 'Employee not found'}, 404
        employee.delete_instance()
        return '', 204

class PDFGenerationResource(Resource):
    def get(self, employee_id):
        try:
            employee = Employee.get(Employee.id == employee_id)
        except Employee.DoesNotExist:
            return {'error': 'Employee not found'}, 404

        # Crear contenido del PDF
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .container {{ padding: 20px; }}
                .header {{ font-size: 24px; font-weight: bold; }}
                .details {{ margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">Employee Details</div>
                <div class="details">
                    <p><strong>Name:</strong> {employee.name}</p>
                    <p><strong>Department:</strong> {employee.department}</p>
                    <p><strong>Email:</strong> {employee.email}</p>
                </div>
            </div>
        </body>
        </html>
        """

        # Generar el PDF
        pdf = pdfkit.from_string(html_content, False)

        # Enviar el PDF como respuesta
        return send_file(io.BytesIO(pdf), as_attachment=True, download_name=f"employee_{employee_id}.pdf")
