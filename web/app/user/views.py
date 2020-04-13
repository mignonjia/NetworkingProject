from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import user
from ..forms import RecordForm, EditRecordForm
from .. import db
from .forms import EmployeeInfoForm, EditEmployeeInfoForm
from ..models import Employee, Record

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
    
    employee = Employee.query.get_or_404(id)
    form = EmployeeInfoForm(
        email=employee.email,
        username=employee.username,
        first_name=employee.first_name,
        last_name=employee.last_name,
        age=employee.age,
        gender=employee.gender,
        health_status=employee.health_status,
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
    employee = Employee.query.get_or_404(id)
    '''
    form = EditEmployeeInfoForm(
        email=employee.email,
        username=employee.username,
        first_name=employee.first_name,
        last_name=employee.last_name,
        age=employee.age,
        gender=employee.gender,
        health_status=employee.health_status,
        )
    '''
    form = EditEmployeeInfoForm(obj=employee)
    form.gender =  employee.gender
    if form.validate_on_submit():
        employee.email = form.email.data
        employee.username = form.username.data
        employee.first_name = form.first_name.data
        employee.last_name = form.last_name.data
        employee.age = form.age.data
        employee.gender = form.gender
        employee.health_status = form.health_status.data
        db.session.commit()
        flash('You have successfully edited the record.')

        # redirect to the records page
        return redirect(url_for('user.profile', edit=False, id=employee.id))
        
    form.email = employee.email
    form.username = employee.username
    form.first_name = employee.first_name
    form.last_name = employee.last_name
    form.age = employee.age
    form.gender =  employee.gender
    form.health_status = employee.health_status
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
    
    employee = Employee.query.get_or_404(id)
    
    records = db.session.query(Record).filter(Record.employee_id==id)
    
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
    
    employee = db.session.query(Employee).filter(Employee.id==id)
    # TODO: set default value of employee to current user.
    form = EditRecordForm(employee=employee)
    
    if form.validate_on_submit():
        record = Record(name=form.name.data,
            description=form.description.data,
            employee=form.employee.data)
        # TODO: check if record.employee = id
        try:
            db.session.add(record)
            db.session.commit()
            flash('You have successfully added a new record.')
        except:
            # in case record name already exists
            flash('Error: record name already exists.')
        # redirect to records page
        return redirect(url_for('user.list_records', id=id))

    # load record template
    return render_template('user/records/record.html', action="Add",
                           add_record=add_record, form=form,
                           title="Add Record")
        

@user.route('/records/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_record(id):
    """
    Edit a record
    """
    check_user()

    add_record = False

    record = Record.query.get_or_404(id)
    form = EditRecordForm(obj=record)
    if form.validate_on_submit():
        record.name = form.name.data
        record.description = form.description.data
        record.employee = form.employee.data
        db.session.commit()
        flash('You have successfully edited the record.')

        # redirect to the records page
        return redirect(url_for('user.list_records', id=record.employee_id))

    form.description.data = record.description
    form.name.data = record.name
    return render_template('user/records/record.html', action="Edit",
                           add_record=add_record, form=form,
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
    return redirect(url_for('user.list_records', id=record.employee_id))

    return render_template(title="Delete Record")

