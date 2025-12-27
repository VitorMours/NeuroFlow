from flask_pagedown.fields import PageDownField
from flask_wtf import FlaskForm 
from wtforms import StringField, IntegerField, PasswordField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired 

class BaseAuthForm(FlaskForm):
  email = EmailField("Email", validators=[DataRequired(message="Please type your email")])
  password = PasswordField("Password", validators=[DataRequired(message="Please type your password")])
  submit = SubmitField("Submit", validators=[DataRequired()])

class NoteForm(FlaskForm):
  title = StringField("Title", validators=[DataRequired(message="Please, do not create a titless note...")])
  content = StringField("Content", render_kw={"placeholder":"Type the content of your note..."})
  create = SubmitField("Create Note", validators=[DataRequired()])
  
class NoteEditForm(FlaskForm):
  title = StringField("Title", validators=[DataRequired(message="Please, do not create a titless note...")])
  content = PageDownField("Content", render_kw={"placeholder":"Type the content of your note..."})
  submit = SubmitField("Save Note", validators=[DataRequired()])
    

class TaskForm(FlaskForm):
  task = StringField("Task Name", validators=[DataRequired(message="Please, do not create a nameless task...")], render_kw={"placeholder":"Type the name of your task..."})
  task_description = StringField("Task Description", render_kw={"placeholder":"Type the description of your task..."})
  submit = SubmitField("Create Task", validators=[DataRequired()])