# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager



class Patient(UserMixin, db.Model):
    """
    Create an Patient table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(14), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    
    ##### Fields for health system. #####
    age = db.Column(db.Integer)
    gender = db.Column(db.Enum('Male', 'Female'))
    height = db.Column(db.Integer)
    health_status = db.Column(db.Enum('Normal', 'Confirmed Case', 'Suspected Case'))
    
    #department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    #role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_admin = db.Column(db.Boolean, default=False)
    records = db.relationship('Record', backref='patient', lazy='dynamic')

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Patient: {}{}>'.format(self.first_name, self.last_name)

# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Patient.query.get(int(user_id))

class Record(db.Model):

    __tablename__ = 'records'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60)) 
    # d_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    time = db.Column(db.DateTime, nullable=False) 
    description = db.Column(db.String(200))
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    patient_name = db.Column(db.String(60))

    def __repr__(self):
        return '<Record: {}>'.format(self.name)
