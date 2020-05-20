# app/auth/views.py

from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import auth
from .forms import LoginForm, RegistrationForm
from .. import db
from ..models import Patient

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests to the /register route
    Add an patient to the database through the registration form
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        patient = Patient(
            phone_number=form.phone_number.data,
            username=form.username.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            password=form.password.data,
            age=form.age.data,
            height=form.height.data,
            health_status=form.health_status.data,
            gender=form.gender.data,            
            )

        # add patient to the database
        db.session.add(patient)
        db.session.commit()
        flash('You have successfully registered! You may now login.')

        # redirect to the login page
        return redirect(url_for('auth.login'))

    # load registration template
    return render_template('auth/register.html', form=form, title='Register')

# Edit the login view to redirect to the admin dashboard if patient is an admin

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        # check whether patient exists in the database and whether
        # the password entered matches the password in the database
        patient = Patient.query.filter_by(phone_number=form.phone_number.data).first()
        if patient is not None and patient.verify_password(
                form.password.data):
            # log patient in
            login_user(patient)

            # redirect to the appropriate dashboard page
            if patient.is_admin:
                return redirect(url_for('home.admin_dashboard'))
            else:
                return redirect(url_for('home.dashboard'))

        # when login details are incorrect
        else:
            flash('Invalid phone_number or password.')

    # load login template
    return render_template('auth/login.html', form=form, title='Login')

@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an patient out through the logout link
    """
    logout_user()
    flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for('auth.login'))