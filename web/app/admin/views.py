import time
from flask import abort, flash, redirect, render_template, url_for, request, current_app, session
from flask_login import current_user, login_required

from . import admin
from ..forms import RecordForm, EditRecordForm, PatientInfoForm, SearchForm
from .. import db
from ..models import Patient, Record


def check_admin():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)


# Patient Views

@admin.route('/patients')
@login_required
def list_patients():
    """
    List all patients
    """
    check_admin()

    patients = Patient.query.all()
    return render_template('admin/patients/patients.html',
                           patients=patients, title='Patients')

@admin.route('/patients/check/<int:id>', methods=['GET', 'POST'])
@login_required
def check_patient(id):
    """
    Checks a patient
    """
    check_admin()

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

    owned_records = db.session.query(Record).filter(Record.patient_id==id)
    return render_template('user/profile/profile.html',
                           form=form,
                           Edit=False,
                           title='User Profile')

@admin.route('/patients/checkrec/<int:id>', methods=['GET', 'POST'])
@login_required
def check_patient_records(id):
    """
    Checks a patient
    """
    check_admin()

    patient = Patient.query.get_or_404(id)

    owned_records = db.session.query(Record).filter(Record.patient_id==id)
    return render_template('admin/patients/patient.html',
                           patient=patient,
                           records=owned_records,
                           title='Look into Patient')


# Record views
'''

@admin.route('/records', methods=['GET', 'POST'])
@login_required
def list_records():
    """
    List all records
    """
    check_admin()
    search_content = request.form.get('search_id')
    records = None
    if search_content is not None:
        records = Record.query.filter(Record.patient_name.like("%"+search_content+"%")).all()
    else:        
        records = Record.query.order_by(Record.time.desc()).all()
    # records = Record.query.all()

    return render_template('admin/records/records.html',
                           records=records, title='Records')
'''
@admin.route('/list_paged_records/', methods=['GET', 'POST'], defaults={'page': 1})
@admin.route('/list_paged_records/<int:page>', methods=['GET', 'POST'])
@login_required
def list_paged_records(page):
    """
    List all records
    """
    check_admin()
    records_per_page = current_app.config['POSTS_PER_PAGE']
    
    records = Record.query.order_by(Record.time.desc()).paginate(page=page, per_page=records_per_page, error_out=False)
    print(' >>> form: ', request.form)
    if 'tag' in session or (request.method == 'POST' and 'tag' in request.form):
        if 'tag' in session and (not ('tag' in request.form)):
            tag = session['tag']
        else:
            tag = request.form['tag']
            session['tag'] = tag
            page = 1
            
        search = "%{}%".format(tag)
        records = Record.query.filter(Record.patient_name.like(search)).paginate(page=page, per_page=records_per_page, error_out=True)
        return render_template('admin/records/records.html', records=records, tag=tag)
    return render_template('admin/records/records.html',
                           records=records, 
                           #page_data=records,
                           title='Records')


@admin.route('/records/add', methods=['GET', 'POST'])
@login_required
def add_record():
    """
    Add a record to the database
    """
    check_admin()

    add_record = True

    form = EditRecordForm()
    if form.validate_on_submit():
        record = Record(name=form.name.data,
            description=form.description.data,
            patient=form.patient.data,
            patient_name="null",
            time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        try:
            # add record to the database
            db.session.add(record)
            db.session.commit()
            flash('You have successfully added a new record.')
        except:
            flash('Error!')
            
        patient = Patient.query.get_or_404(record.patient_id)
        if not patient.first_name:
            record.patient_name = "admin"
        else:
            record.patient_name = patient.first_name + " " + patient.last_name
        db.session.commit()

        # redirect to records page
        return redirect(url_for('admin.list_paged_records'))

    # load record template
    return render_template('admin/records/record.html', action="Add",
                           add_record=add_record, form=form,
                           title="Add Record")


@admin.route('/records/show/<int:id>', methods=['GET', 'POST'])
@login_required
def show_record(id):
    """
    Edit a record
    """
    check_admin()

    add_record = False

    record = Record.query.get_or_404(id)
    form = RecordForm(obj=record)

    #form.description.data = record.description
    #form.name.data = record.name
    return render_template('admin/records/record.html', action="Show",
                           add_record=add_record, form=form,
                           title="Show Record")


@admin.route('/records/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_record(id):
    """
    Edit a record
    """
    check_admin()

    add_record = False

    record = Record.query.get_or_404(id)
    form = EditRecordForm(obj=record)
    if form.validate_on_submit():
        record.name = form.name.data
        record.description = form.description.data
        record.patient = form.patient.data
        patient = Patient.query.get_or_404(record.patient_id)
        record.patient_name = (patient.first_name if patient.first_name else "") + " " + (patient.last_name if patient.last_name else " admin ")
        db.session.commit()
        flash('You have successfully edited the record.')

        # redirect to the records page
        return redirect(url_for('admin.list_paged_records'))

    form.description.data = record.description
    form.name.data = record.name
    return render_template('admin/records/record.html', action="Edit",
                           add_record=add_record, form=form,
                           record=record, title="Edit Record")


@admin.route('/records/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_record(id):
    """
    Delete a record from the database
    """
    check_admin()

    record = Record.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    flash('You have successfully deleted the record.')

    # redirect to the records page
    return redirect(url_for('admin.list_paged_records'))

    return render_template(title="Delete Record")

