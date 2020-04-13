from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, TextField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired

class ReadonlyTextField(TextField):
  def __call__(self, *args, **kwargs):
    kwargs.setdefault('readonly', True)
    return super(ReadonlyTextField, self).__call__(*args, **kwargs)
    
class EmployeeInfoForm(FlaskForm):
    """
    Form for an user to edit personal profile.
    """
    email = ReadonlyTextField('Email')
    username = ReadonlyTextField('Username')
    first_name = ReadonlyTextField('First Name')
    last_name = ReadonlyTextField('Last Name')
    
    age = ReadonlyTextField('Age')
    gender = ReadonlyTextField('Gender')
    health_status = ReadonlyTextField('Health Status')

class EditEmployeeInfoForm(FlaskForm):
    """
    Form for an user to edit personal profile.
    """
    email = ReadonlyTextField('Email')
    username = ReadonlyTextField('Username')
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    
    age = IntegerField('Age', validators=[DataRequired()])
    gender = SelectField('Gender', 
        choices=[('female','female'), ('male', 'male')], 
        validators=[DataRequired()],
        coerce=str)
    health_status = SelectField('Health Status', 
        choices=[('Normal','Normal'), ('Confirmed Case', 'Confirmed Case'), ('Suspected Case', 'Suspected Case')], 
        validators=[DataRequired()],
        coerce=str)
    submit = SubmitField('Submit')
