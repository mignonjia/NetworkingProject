import sys
import traceback
import time
from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required

from . import user
from ..forms import RecordForm, EditRecordForm
from .. import db
from ..forms import PatientInfoForm, EditPatientInfoForm
from ..models import Patient, Record

def check_user():
    # prevent non-admins from accessing the page
    if current_user.is_admin:
        abort(403)

@user.route('/profile/<int:id>', methods=['GET', 'POST'])
@login_required
def profile(id):
    """
    List all records
    """
    
    check_user()
    
    patient = Patient.query.get_or_404(id)
    form = PatientInfoForm(
        phone_number=patient.phone_number,
        username=patient.username,
        first_name=patient.first_name,
        last_name=patient.last_name,
        age=patient.age,
        height=patient.height,
        gender=patient.gender,
        health_status=patient.health_status,
        )
    
    return render_template('user/profile/profile.html',
                           form=form, 
                           edit=False,
                           title='Profile')
                           
    check_user()

@user.route('/profile/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_profile(id):
    """
    List all records
    """
    
    check_user()
    patient = Patient.query.get_or_404(id)
    form = EditPatientInfoForm(obj=patient)
    form.gender =  patient.gender
    if form.validate_on_submit():
        patient.phone_number = form.phone_number.data
        patient.username = form.username.data
        patient.first_name = form.first_name.data
        patient.last_name = form.last_name.data
        patient.age = form.age.data
        patient.height = form.height.data
        patient.gender = form.gender
        patient.health_status = form.health_status.data
        db.session.commit()
        
        flash('You have successfully edited the record.')

        # redirect to the records page
        return redirect(url_for('user.profile', edit=False, id=patient.id))
        
    form.phone_number = patient.phone_number
    form.username = patient.username
    form.first_name = patient.first_name
    form.last_name = patient.last_name
    form.age = patient.age
    form.height = patient.height
    form.gender =  patient.gender
    form.health_status = patient.health_status
    edit = True
    return render_template('user/profile/profile.html', 
                           form=form,
                           edit=edit,
                           title="Edit Profile")

@user.route('/records/<int:id>', methods=['GET', 'POST'])
@login_required
def list_records(id):
    """
    List all records
    """
    
    check_user()
    
    patient = Patient.query.get_or_404(id)
    
    records = db.session.query(Record).filter(Record.patient_id==id)
    
    return render_template('user/records/records.html',
                           records=records, title='Records')

@user.route('/records/add/<int:id>', methods=['GET', 'POST'])
@login_required
def add_record(id):
    """
    Add a record to the database
    """
    check_user()
    add_record = True
    
    #patient = db.session.query(Patient).filter(Patient.id==id)
    # TODO: set default value of Patient to current user.
    
    if request.method == 'POST':
        print(request.form)
        lat = request.form['Latitude']
        log = request.form['Longitude']
        record = Record(name=request.form['Name'],
            description=request.form['Description'],
            patient_id=id,
            time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            log=log,
            lat=lat)
        # TODO: check if record.Patient = id
        try:
            db.session.add(record)
            db.session.commit()
            flash('You have successfully added a new record.')
        except:
            flash('Error.\n', record.patient.username, ' ' , record.name, ' ' , record.time,  ' ', record.description)
            #flash(str(e), '  === \n', e.message)
            traceback.print_exc()
        # redirect to records page
        return redirect(url_for('user.list_records', id=id))

    # load record template
    else:
        return render_template('user/records/record.html', action="Add",
                           add_record=add_record,
                           title="Add Record")
@user.route('/records/show/<int:id>', methods=['GET', 'POST'])
@login_required
def show_record(id):
    """
    Edit a record
    """
    check_user()
    record = Record.query.get_or_404(id)
    print(' rec: ', record.lat)
    form = RecordForm(obj=record)
    print(' rec: ', form.lat)
    
    return render_template('user/records/record.html', action="Show",
                           add_record=False, 
                           edit_record=False, 
                           record=record, 
                           form=form,
                           id=record.id,
                           title="Show Record")


@user.route('/records/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_record(id):
    """
    Edit a record
    """
    check_user()

    add_record = False
    edit_record = True

    record = Record.query.get_or_404(id)
    form = EditRecordForm(obj=record)
    if form.validate_on_submit():
        record.name = form.name.data
        record.time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        record.description = form.description.data
        record.patient = form.patient.data
        db.session.commit()
        flash('You have successfully edited the record.')

        # redirect to the records page
        return redirect(url_for('user.list_records', id=record.patient_id))

    form.description.data = record.description
    form.name.data = record.name
    return render_template('user/records/record.html', action="Edit",
                           add_record=add_record, edit_record=edit_record, form=form,
                           record=record, title="Edit Record")


@user.route('/records/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_record(id):
    """
    Delete a record from the database
    """
    check_user()

    record = Record.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    flash('You have successfully deleted the record.')

    # redirect to the records page
    return redirect(url_for('user.list_records', id=record.patient_id))

    return render_template(title="Delete Record")

@user.route('/blockchain/<int:id>', methods=['GET', 'POST'])
@login_required
def blockchain(id):
    return render_template('user/blockchain/blockchain.html')