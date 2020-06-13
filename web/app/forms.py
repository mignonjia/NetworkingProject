from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, SelectField, TextField, DecimalField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Email
from wtforms import validators

from .models import Record, Patient

class ReadonlyTextField(TextField):
  def __call__(self, *args, **kwargs):
    kwargs.setdefault('readonly', True)
    return super(ReadonlyTextField, self).__call__(*args, **kwargs)


class ReadonlyDecimalField(DecimalField):
  def __call__(self, *args, **kwargs):
    kwargs.setdefault('readonly', True)
    return super(ReadonlyDecimalField, self).__call__(*args, **kwargs)


    
class RecordForm(FlaskForm):
    """
    Form for users to view physical examination results.
    """
    name = ReadonlyTextField('Name')
    time = ReadonlyTextField('Time')
    patient = ReadonlyTextField()
    description = ReadonlyTextField('Description')
    lat = ReadonlyDecimalField('Latitude')
    log = ReadonlyDecimalField('Longitude')
    
class EditRecordForm(FlaskForm):
    """
    Form for users to upload physical examination results.
    """
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    patient = QuerySelectField(
        query_factory=lambda: Patient.query.all(), get_label="username")
        
    lat = DecimalField('Latitude', validators=[validators.optional()])
    log = DecimalField('Longitude', validators=[validators.optional()])
    
    submit = SubmitField('Submit')
    
    

class PatientInfoForm(FlaskForm):
    """
    Form for an user to view personal profile.
    """
    phone_number = ReadonlyTextField('Phone Number')
    username = ReadonlyTextField('Username')
    first_name = ReadonlyTextField('First Name')
    last_name = ReadonlyTextField('Last Name')
    
    age = ReadonlyTextField('Age')
    height = ReadonlyTextField('Height')
    gender = ReadonlyTextField('Gender')
    health_status = ReadonlyTextField('Health Status')

class EditPatientInfoForm(FlaskForm):
    """
    Form for an user to edit personal profile.
    """
    phone_number = ReadonlyTextField('Phone Number')
    username = ReadonlyTextField('Username')
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    
    age = IntegerField('Age', validators=[DataRequired()])
    height = IntegerField('Height', validators=[DataRequired()])
    gender = SelectField('Gender', 
        choices=[('female','female'), ('male', 'male')], 
        validators=[DataRequired()],
        coerce=str)
    health_status = SelectField('Health Status', 
        choices=[('Normal','Normal'), ('Confirmed Case', 'Confirmed Case'), ('Suspected Case', 'Suspected Case')], 
        validators=[DataRequired()],
        coerce=str)
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):
    search_keyword = StringField('name of user', validators = [DataRequired()])
    submit = SubmitField('Search')
    
