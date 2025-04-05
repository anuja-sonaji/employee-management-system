from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from models import Employee, User, Feedback
from datetime import datetime
import pandas as pd
import os
import logging
from utils import require_manager, export_employees_to_excel

logger = logging.getLogger(__name__)
employee_bp = Blueprint('employee', __name__)

@employee_bp.route('/')
@login_required
def dashboard():
    # Basic statistics for the dashboard
    total_employees = Employee.query.count()
    # Add current date/time for dashboard display
    now = datetime.now()
    
    # For managers, show their team stats
    if current_user.is_manager:
        managed_employees = Employee.query.filter_by(manager_id=current_user.id).count()
        recent_feedback = Feedback.query.filter_by(provided_by_id=current_user.id)\
            .order_by(Feedback.feedback_date.desc()).limit(5).all()
        
        # Team distribution by skill
        team_skills = db.session.query(Employee.skill, db.func.count(Employee.id))\
            .filter_by(manager_id=current_user.id)\
            .group_by(Employee.skill).all()
        
        context = {
            'total_employees': total_employees,
            'managed_employees': managed_employees,
            'recent_feedback': recent_feedback,
            'team_skills': team_skills,
            'is_manager': True,
            'now': now
        }
    else:
        # For regular employees, show their feedback
        employee = Employee.query.filter_by(user_id=current_user.id).first()
        
        if employee:
            recent_feedback = Feedback.query.filter_by(employee_id=employee.id)\
                .order_by(Feedback.feedback_date.desc()).limit(5).all()
            
            context = {
                'total_employees': total_employees,
                'employee': employee,
                'recent_feedback': recent_feedback,
                'is_manager': False,
                'now': now
            }
        else:
            context = {
                'total_employees': total_employees,
                'is_manager': False,
                'now': now
            }
    
    return render_template('dashboard.html', **context)

@employee_bp.route('/employees')
@login_required
def employee_list():
    # Filter employees based on user's role
    if current_user.is_manager:
        # Managers see all employees, but highlight their team
        employees = Employee.query.all()
    else:
        # Regular employees only see themselves
        employee = Employee.query.filter_by(user_id=current_user.id).first()
        employees = [employee] if employee else []
    
    # Get all managers for the dropdown in templates
    managers = User.query.filter_by(is_manager=True).all()
    
    return render_template('employee_list.html', 
                           employees=employees, 
                           managers=managers,
                           is_manager=current_user.is_manager)

@employee_bp.route('/employees/<int:employee_id>')
@login_required
def employee_detail(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    
    # Regular employees can only view their own details
    if not current_user.is_manager and not employee.user_id == current_user.id:
        flash('You do not have permission to view this employee.', 'danger')
        return redirect(url_for('employee.employee_list'))
    
    # Get feedback for the employee
    feedback = Feedback.query.filter_by(employee_id=employee.id)\
        .order_by(Feedback.feedback_date.desc()).all()
    
    # Get manager info
    manager = User.query.get(employee.manager_id) if employee.manager_id else None
    
    return render_template('employee_detail.html', 
                           employee=employee, 
                           feedback=feedback,
                           manager=manager,
                           is_manager=current_user.is_manager)

@employee_bp.route('/employees/new', methods=['GET', 'POST'])
@login_required
@require_manager
def create_employee():
    if request.method == 'POST':
        try:
            # Get form data
            full_name = request.form.get('full_name')
            joining_date_str = request.form.get('joining_date')
            benzyl = request.form.get('benzyl')
            role = request.form.get('role')
            skill = request.form.get('skill')
            team = request.form.get('team')
            grade = request.form.get('grade')
            designation = request.form.get('designation')
            location = request.form.get('location')
            manager_id = request.form.get('manager_id')
            
            # Validate required fields
            if not all([full_name, joining_date_str, benzyl, role, skill, team, grade, designation, location]):
                flash('All fields are required', 'danger')
                return redirect(url_for('employee.create_employee'))
            
            # Convert joining date string to date object
            joining_date = datetime.strptime(joining_date_str, '%Y-%m-%d').date()
            
            # Create new employee
            new_employee = Employee(
                full_name=full_name,
                joining_date=joining_date,
                benzyl=benzyl,
                role=role,
                skill=skill,
                team=team,
                grade=grade,
                designation=designation,
                location=location,
                manager_id=manager_id if manager_id else current_user.id
            )
            
            db.session.add(new_employee)
            db.session.commit()
            
            flash('Employee created successfully', 'success')
            return redirect(url_for('employee.employee_detail', employee_id=new_employee.id))
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating employee: {str(e)}")
            flash(f'Error creating employee: {str(e)}', 'danger')
    
    # Get all managers for the dropdown
    managers = User.query.filter_by(is_manager=True).all()
    
    return render_template('employee_form.html', 
                           employee=None,
                           managers=managers,
                           action='create')

@employee_bp.route('/employees/<int:employee_id>/edit', methods=['GET', 'POST'])
@login_required
@require_manager
def edit_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    
    if request.method == 'POST':
        try:
            # Update employee data from form
            employee.full_name = request.form.get('full_name')
            employee.joining_date = datetime.strptime(request.form.get('joining_date'), '%Y-%m-%d').date()
            employee.benzyl = request.form.get('benzyl')
            employee.role = request.form.get('role')
            employee.skill = request.form.get('skill')
            employee.team = request.form.get('team')
            employee.grade = request.form.get('grade')
            employee.designation = request.form.get('designation')
            employee.location = request.form.get('location')
            employee.manager_id = request.form.get('manager_id')
            
            db.session.commit()
            flash('Employee updated successfully', 'success')
            return redirect(url_for('employee.employee_detail', employee_id=employee.id))
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating employee: {str(e)}")
            flash(f'Error updating employee: {str(e)}', 'danger')
    
    # Get all managers for the dropdown
    managers = User.query.filter_by(is_manager=True).all()
    
    return render_template('employee_form.html', 
                           employee=employee,
                           managers=managers,
                           action='edit')

@employee_bp.route('/employees/<int:employee_id>/delete', methods=['POST'])
@login_required
@require_manager
def delete_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    
    try:
        # Also delete related feedback
        Feedback.query.filter_by(employee_id=employee.id).delete()
        
        db.session.delete(employee)
        db.session.commit()
        flash('Employee deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting employee: {str(e)}")
        flash(f'Error deleting employee: {str(e)}', 'danger')
    
    return redirect(url_for('employee.employee_list'))

@employee_bp.route('/import-export', methods=['GET', 'POST'])
@login_required
@require_manager
def import_export():
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'import':
            # Check if file was uploaded
            if 'file' not in request.files:
                flash('No file part', 'danger')
                return redirect(request.url)
            
            file = request.files['file']
            
            # Check if file was selected
            if file.filename == '':
                flash('No file selected', 'danger')
                return redirect(request.url)
            
            # Check file extension
            if file and file.filename.endswith(('.xlsx', '.xls', '.csv')):
                try:
                    # Read Excel/CSV file
                    if file.filename.endswith('.csv'):
                        df = pd.read_csv(file)
                    else:
                        df = pd.read_excel(file)
                    
                    # Process data
                    imported_count = 0
                    for _, row in df.iterrows():
                        # Check if employee exists
                        existing_employee = Employee.query.filter_by(benzyl=row.get('Benzyl')).first()
                        
                        # Convert joining date
                        joining_date = None
                        joining_date_str = row.get('Joining Date')
                        if isinstance(joining_date_str, str):
                            try:
                                joining_date = datetime.strptime(joining_date_str, '%d-%m-%Y').date()
                            except ValueError:
                                try:
                                    joining_date = datetime.strptime(joining_date_str, '%Y-%m-%d').date()
                                except ValueError:
                                    logger.warning(f"Could not parse date: {joining_date_str}")
                        elif isinstance(joining_date_str, pd.Timestamp):
                            joining_date = joining_date_str.date()
                        
                        if not joining_date:
                            continue
                        
                        if existing_employee:
                            # Update existing employee
                            existing_employee.full_name = row.get('Full Name')
                            existing_employee.joining_date = joining_date
                            existing_employee.role = row.get('Role')
                            existing_employee.skill = row.get('Skill')
                            existing_employee.team = row.get('Team')
                            existing_employee.grade = row.get('Grade')
                            existing_employee.designation = row.get('Designation')
                            existing_employee.location = row.get('Location')
                        else:
                            # Create new employee
                            manager_name = row.get('Manager Name')
                            manager = User.query.filter_by(username=manager_name).first()
                            
                            new_employee = Employee(
                                full_name=row.get('Full Name'),
                                joining_date=joining_date,
                                benzyl=row.get('Benzyl'),
                                role=row.get('Role'),
                                skill=row.get('Skill'),
                                team=row.get('Team'),
                                grade=row.get('Grade'),
                                designation=row.get('Designation'),
                                location=row.get('Location'),
                                manager_id=manager.id if manager else current_user.id
                            )
                            db.session.add(new_employee)
                        
                        imported_count += 1
                    
                    db.session.commit()
                    flash(f'Successfully imported {imported_count} employees', 'success')
                    
                except Exception as e:
                    db.session.rollback()
                    logger.error(f"Error importing employees: {str(e)}")
                    flash(f'Error importing employees: {str(e)}', 'danger')
            else:
                flash('File format not supported. Please upload an Excel or CSV file.', 'danger')
        
        elif action == 'export':
            try:
                # Export all employees to Excel
                excel_file = export_employees_to_excel()
                
                flash('Employee data exported successfully', 'success')
                return excel_file
            except Exception as e:
                logger.error(f"Error exporting employees: {str(e)}")
                flash(f'Error exporting employees: {str(e)}', 'danger')
    
    return render_template('import_export.html')
