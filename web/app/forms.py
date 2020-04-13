from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, SelectField, TextField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Email

from .models import Department, Role, Employee

class ReadonlyTextField(TextField):
  def __call__(self, *args, **kwargs):
    kwargs.setdefault('readonly', True)
    return super(ReadonlyTextField, self).__call__(*args, **kwargs)

class DepartmentForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class RoleForm(FlaskForm):
    """
    Form for admin to add or edit a role
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class EmployeeAssignForm(FlaskForm):
    """
    Form for admin to assign departments and roles to employees
    """
    department = QuerySelectField(query_factory=lambda: Department.query.all(),
                                  get_label="name")
    role = QuerySelectField(query_factory=lambda: Role.query.all(),
                            get_label="name")
    submit = SubmitField('Submit')
    

    
class RecordForm(FlaskForm):
    """
    Form for users to upload physical examination results.
    """
    name = ReadonlyTextField('Name')
    description = ReadonlyTextField('Description')
    employee = ReadonlyTextField()
    
class EditRecordForm(FlaskForm):
    """
    Form for users to upload physical examination results.
    """
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    employee = QuerySelectField(
        query_factory=lambda: Employee.query.all(), get_label="username")
    submit = SubmitField('Submit')
    
    
