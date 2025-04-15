from functools import wraps
from flask import flash, redirect, url_for, Response
from flask_login import current_user
from datetime import datetime
import pandas as pd
import io
from models import Employee, User

def require_manager(f):
    """Decorator to require manager role for a view"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_manager:
            flash('This action requires manager privileges', 'danger')
            return redirect(url_for('employee.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def get_current_month():
    now = datetime.utcnow()
    return f"{now.year:04d}-{now.month:02d}"

def export_employees_to_excel():
    """Export employee data to Excel"""
    # Query all employees
    employees = Employee.query.all()

    # Create dataframe
    data = []
    for employee in employees:
        manager = User.query.get(employee.manager_id) if employee.manager_id else None
        manager_name = manager.username if manager else ""

        data.append({
            'Full Name': employee.full_name,
            'Joining Date': employee.joining_date,
            'Benzyl': employee.benzyl,
            'Role': employee.role,
            'Skill': employee.skill,
            'Team': employee.team,
            'Manager Name': manager_name,
            'Grade': employee.grade,
            'Designation': employee.designation,
            'Location': employee.location
        })

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Create Excel file in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Employees')

    output.seek(0)

    # Create response with Excel file
    return Response(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={
            'Content-Disposition': 'attachment; filename=employee_data.xlsx'
        }
    )