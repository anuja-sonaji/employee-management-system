from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from app import db
from models import User, Employee
import logging

logger = logging.getLogger(__name__)
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('employee.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Validate form inputs
        if not username or not password:
            flash('Please provide both username and password', 'danger')
            return render_template('login.html')
        
        # Find user by username
        user = User.query.filter_by(username=username).first()
        
        # Check if user exists and password is correct
        if user and user.check_password(password):
            login_user(user)
            logger.info(f"User {username} logged in successfully")
            
            # Redirect to the page user was trying to access or dashboard
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('employee.dashboard'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')
            logger.warning(f"Failed login attempt for username: {username}")
    
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile')
@login_required
def profile():
    # Find employee record related to this user if it exists
    employee = Employee.query.filter_by(user_id=current_user.id).first()
    return render_template('profile.html', employee=employee)

# Admin function to create initial users
@auth_bp.route('/create_initial_users')
def create_initial_users():
    # Check if any users exist already
    if User.query.count() > 0:
        flash('Initial users already created', 'info')
        return redirect(url_for('auth.login'))
    
    try:
        # Create admin user
        admin = User(
            username='admin',
            email='admin@example.com',
            is_manager=True
        )
        admin.set_password('admin123')
        
        # Create a regular employee user
        employee = User(
            username='employee',
            email='employee@example.com',
            is_manager=False
        )
        employee.set_password('employee123')
        
        db.session.add(admin)
        db.session.add(employee)
        db.session.commit()
        
        flash('Initial users created successfully. You can now login with username "admin" and password "admin123".', 'success')
        logger.info("Initial users created")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating initial users: {str(e)}")
        flash(f'Error creating users: {str(e)}', 'danger')
    
    return redirect(url_for('auth.login'))
