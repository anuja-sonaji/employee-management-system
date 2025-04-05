from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from models import Employee, Feedback
from datetime import datetime
import logging
from utils import require_manager, get_current_quarter

logger = logging.getLogger(__name__)
feedback_bp = Blueprint('feedback', __name__, url_prefix='/feedback')

@feedback_bp.route('/')
@login_required
def feedback_list():
    # For managers, show feedback they've given
    if current_user.is_manager:
        feedback = Feedback.query.filter_by(provided_by_id=current_user.id)\
            .order_by(Feedback.feedback_date.desc()).all()
        
        context = {
            'feedback': feedback,
            'is_manager': True,
            'view_type': 'provided'
        }
    else:
        # For employees, show feedback they've received
        employee = Employee.query.filter_by(user_id=current_user.id).first()
        
        if employee:
            feedback = Feedback.query.filter_by(employee_id=employee.id)\
                .order_by(Feedback.feedback_date.desc()).all()
            
            context = {
                'feedback': feedback,
                'is_manager': False,
                'view_type': 'received'
            }
        else:
            context = {
                'feedback': [],
                'is_manager': False,
                'view_type': 'received'
            }
    
    return render_template('feedback_list.html', **context)

@feedback_bp.route('/employee/<int:employee_id>')
@login_required
def employee_feedback(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    
    # Regular employees can only view their own feedback
    if not current_user.is_manager and not employee.user_id == current_user.id:
        flash('You do not have permission to view this feedback.', 'danger')
        return redirect(url_for('feedback.feedback_list'))
    
    # Get feedback for the employee
    feedback = Feedback.query.filter_by(employee_id=employee.id)\
        .order_by(Feedback.feedback_date.desc()).all()
    
    return render_template('feedback_list.html', 
                           feedback=feedback,
                           employee=employee,
                           is_manager=current_user.is_manager,
                           view_type='for_employee')

@feedback_bp.route('/new/<int:employee_id>', methods=['GET', 'POST'])
@login_required
@require_manager
def create_feedback(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    
    # Make sure the employee is managed by the current user
    if employee.manager_id != current_user.id:
        flash('You can only provide feedback for employees you manage.', 'danger')
        return redirect(url_for('employee.employee_list'))
    
    if request.method == 'POST':
        try:
            # Get form data
            rating = int(request.form.get('rating'))
            feedback_text = request.form.get('feedback_text')
            quarter = request.form.get('quarter')
            
            # Validate required fields
            if not all([rating, feedback_text, quarter]):
                flash('All fields are required', 'danger')
                return redirect(url_for('feedback.create_feedback', employee_id=employee_id))
            
            # Validate rating range
            if rating < 1 or rating > 5:
                flash('Rating must be between 1 and 5', 'danger')
                return redirect(url_for('feedback.create_feedback', employee_id=employee_id))
            
            # Create new feedback
            new_feedback = Feedback(
                employee_id=employee_id,
                provided_by_id=current_user.id,
                rating=rating,
                feedback_text=feedback_text,
                quarter=quarter,
                feedback_date=datetime.utcnow()
            )
            
            db.session.add(new_feedback)
            db.session.commit()
            
            flash('Feedback submitted successfully', 'success')
            return redirect(url_for('feedback.employee_feedback', employee_id=employee_id))
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating feedback: {str(e)}")
            flash(f'Error submitting feedback: {str(e)}', 'danger')
    
    # Get current quarter for default selection
    current_quarter = get_current_quarter()
    
    return render_template('feedback_form.html', 
                           employee=employee,
                           current_quarter=current_quarter,
                           feedback=None,
                           action='create')

@feedback_bp.route('/edit/<int:feedback_id>', methods=['GET', 'POST'])
@login_required
@require_manager
def edit_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    
    # Make sure the feedback was provided by the current user
    if feedback.provided_by_id != current_user.id:
        flash('You can only edit feedback you provided.', 'danger')
        return redirect(url_for('feedback.feedback_list'))
    
    employee = Employee.query.get(feedback.employee_id)
    
    if request.method == 'POST':
        try:
            # Update feedback data from form
            feedback.rating = int(request.form.get('rating'))
            feedback.feedback_text = request.form.get('feedback_text')
            feedback.quarter = request.form.get('quarter')
            
            # Validate rating range
            if feedback.rating < 1 or feedback.rating > 5:
                flash('Rating must be between 1 and 5', 'danger')
                return redirect(url_for('feedback.edit_feedback', feedback_id=feedback_id))
            
            db.session.commit()
            flash('Feedback updated successfully', 'success')
            return redirect(url_for('feedback.employee_feedback', employee_id=employee.id))
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating feedback: {str(e)}")
            flash(f'Error updating feedback: {str(e)}', 'danger')
    
    return render_template('feedback_form.html', 
                           employee=employee,
                           feedback=feedback,
                           action='edit')

@feedback_bp.route('/delete/<int:feedback_id>', methods=['POST'])
@login_required
@require_manager
def delete_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    
    # Make sure the feedback was provided by the current user
    if feedback.provided_by_id != current_user.id:
        flash('You can only delete feedback you provided.', 'danger')
        return redirect(url_for('feedback.feedback_list'))
    
    employee_id = feedback.employee_id
    
    try:
        db.session.delete(feedback)
        db.session.commit()
        flash('Feedback deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting feedback: {str(e)}")
        flash(f'Error deleting feedback: {str(e)}', 'danger')
    
    return redirect(url_for('feedback.employee_feedback', employee_id=employee_id))
