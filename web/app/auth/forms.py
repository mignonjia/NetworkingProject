# app/auth/forms.py

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo

from ..models import Patient

class RegistrationForm(FlaskForm):
    """
    Form for users to create new account
    """
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
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
    
    password = PasswordField('Password', validators=[
                                        DataRequired(),
                                        EqualTo('confirm_password')
                                        ])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Register')

    def validate_phone_number(self, field):
        if Patient.query.filter_by(phone_number=field.data).first():
            raise ValidationError('Phone number is already in use.')

    def validate_username(self, field):
        if Patient.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already in use.')

class LoginForm(FlaskForm):
    """
    Form for users to login
    """
    phone_number = StringField('Phone Number', validators=[DataRequired()]) #TODO: validate.
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    