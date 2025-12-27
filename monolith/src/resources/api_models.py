from flask_restx import fields

user_model = {
    "uuid": fields.String,
    "first_name":fields.String,
    "last_name": fields.String, 
    "email": fields.String,
}

user_model_creation = {
    "first_name":fields.String,
    "last_name": fields.String, 
    "email": fields.String,
    "password": fields.String
}

task_model = {
    "uuid":fields.String,
    "task":fields.String,
    "task_description":fields.String,
    "task_conclusion":fields.Boolean,
    "user_id":fields.String
}


task_model_creation = {
    "task":fields.String,
    "task_description":fields.String,
    "user_id":fields.String
}