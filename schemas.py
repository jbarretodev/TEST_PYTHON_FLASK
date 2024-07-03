from marshmallow import Schema, fields, validate, ValidationError

class Employee_Schema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=4, max=100))
    department = fields.String(required=True, validate=validate.Length(min=4, max=100))
    email = fields.Email(required=True, validate=validate.Length(min=8, max=100))

    class Meta:
        strict = True
