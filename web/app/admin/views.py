from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from ..forms import DepartmentForm, EmployeeAssignForm, RoleForm, RecordForm, EditRecordForm
from .. import db
from ..models import Department, Employee, Role, Record


def check_admin():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)


# Department Views


@admin.route('/departments', methods=['GET', 'POST'])
@login_required
def list_departments():
    """
    List all departments
    """
    check_admin()

    departments = Department.query.all()

    return render_template('admin/departments/departments.html',
                           departments=departments, title="Departments")


@admin.route('/departments/add', methods=['GET', 'POST'])
@login_required
def add_department():
    """
    Add a department to the database
    """
    check_admin()

    add_department = True

    form = DepartmentForm()
    if form.validate_on_submit():
        department = Department(name=form.name.data,
                                description=form.description.data)
        try:
            # add department to the database
            db.session.add(department)
            db.session.commit()
            flash('You have successfully added a new department.')
        except:
            # in case department name already exists
            flash('Error: department name already exists.')

        # redirect to departments page
        return redirect(url_for('admin.list_departments'))

    # load department template
    return render_template('admin/departments/department.html', action="Add",
                           add_department=add_department, form=form,
                           title="Add Department")


@admin.route('/departments/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    """
    Edit a department
    """
    check_admin()

    add_department = False

    department = Department.query.get_or_404(id)
    form = DepartmentForm(obj=department)
    if form.validate_on_submit():
        department.name = form.name.data
        department.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the department.')

        # redirect to the departments page
        return redirect(url_for('admin.list_departments'))

    form.description.data = department.description
    form.name.data = department.name
    return render_template('admin/departments/department.html', action="Edit",
                           add_department=add_department, form=form,
                           department=department, title="Edit Department")


@admin.route('/departments/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_department(id):
    """
    Delete a department from the database
    """
    check_admin()

    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    flash('You have successfully deleted the department.')

    # redirect to the departments page
    return redirect(url_for('admin.list_departments'))

    return render_template(title="Delete Department")


# Role Views


@admin.route('/roles')
@login_required
def list_roles():
    check_admin()
    """
    List all roles
    """
    roles = Role.query.all()
    return render_template('admin/roles/roles.html',
                           roles=roles, title='Roles')


@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    """
    Add a role to the database
    """
    check_admin()

    add_role = True

    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data,
                    description=form.description.data)

        try:
            # add role to the database
            db.session.add(role)
            db.session.commit()
            flash('You have successfully added a new role.')
        except:
            # in case role name already exists
            flash('Error: role name already exists.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    # load role template
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title='Add Role')


@admin.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    """
    Edit a role
    """
    check_admin()

    add_role = False

    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        db.session.add(role)
        db.session.commit()
        flash('You have successfully edited the role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    form.description.data = role.description
    form.name.data = role.name
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title="Edit Role")


@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    """
    Delete a role from the database
    """
    check_admin()

    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('You have successfully deleted the role.')

    # redirect to the roles page
    return redirect(url_for('admin.list_roles'))

    return render_template(title="Delete Role")


# Employee Views

@admin.route('/employees')
@login_required
def list_employees():
    """
    List all employees
    """
    check_admin()

    employees = Employee.query.all()
    return render_template('admin/employees/employees.html',
                           employees=employees, title='Employees')


@admin.route('/employees/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_employee(id):
    """
    Assign a department and a role to an employee
    """
    check_admin()

    employee = Employee.query.get_or_404(id)

    # prevent admin from being assigned a department or role
    if employee.is_admin:
        abort(403)

    form = EmployeeAssignForm(obj=employee)
    if form.validate_on_submit():
        employee.department = form.department.data
        employee.role = form.role.data
        db.session.add(employee)
        db.session.commit()
        flash('You have successfully assigned a department and role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_employees'))

    return render_template('admin/employees/employee_assign.html',
                           employee=employee, form=form,
                           title='Assign Employee')
                           

@admin.route('/employees/check/<int:id>', methods=['GET', 'POST'])
@login_required
def check_employee(id):
    """
    Checks an employee
    """
    check_admin()

    employee = Employee.query.get_or_404(id)

    # prevent admin from being assigned a department or role
    if employee.is_admin:
        abort(403)

    form = EmployeeAssignForm(obj=employee)
    if form.validate_on_submit():
        employee.department = form.department.data
        employee.role = form.role.data
        db.session.add(employee)
        db.session.commit()
        flash('You have successfully assigned a department and role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_employees'))

    owned_records = db.session.query(Record).filter(Record.employee_id==id)
    return render_template('admin/employees/employee.html',
                           employee=employee, form=form,
                           records=owned_records,
                           title='Look into Employee')
                           
                           
# Record views


@admin.route('/records', methods=['GET', 'POST'])
@login_required
def list_records():
    """
    List all records
    """
    check_admin()

    records = Record.query.all()

    return render_template('admin/records/records.html',
                           records=records, title='Records')


@admin.route('/records/add', methods=['GET', 'POST'])
@login_required
def add_record():
    """
    Add a record to the database
    """
    check_admin()

    add_record = True

    form = RecordForm()
    if form.validate_on_submit():
        record = Record(name=form.name.data,
            description=form.description.data,
            employee=form.employee.data)
        try:
            # add record to the database
            db.session.add(record)
            db.session.commit()
            flash('You have successfully added a new record.')
        except:
            # in case record name already exists
            flash('Error: record name already exists.')

        # redirect to records page
        return redirect(url_for('admin.list_records'))

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
                           record=record, title="Show Record")


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
        record.employee = form.employee.data
        db.session.commit()
        flash('You have successfully edited the record.')

        # redirect to the records page
        return redirect(url_for('admin.list_records'))

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
    return redirect(url_for('admin.list_records'))

    return render_template(title="Delete Record")

