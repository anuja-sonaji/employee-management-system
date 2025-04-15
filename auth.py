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
        username = request.form.get('username').lower()
        password = request.form.get('password')

        # Check if user exists and is a manager
        user = User.query.filter_by(username=username, is_manager=True).first()
        
        if user and password == 'LM123':
            login_user(user)
            flash('Welcome, Line Manager!', 'success')
            return redirect(url_for('employee.dashboard'))
        else:
            flash('Invalid credentials. Please use your name as username and LM123 as password.', 'danger')

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
        # Create line manager users with their actual names
        managers = [
            {'username': 'anuja', 'email': 'anuja@example.com'},
            {'username': 'sooraj', 'email': 'sooraj@example.com'},
            {'username': 'asha', 'email': 'asha@example.com'},
            {'username': 'vinod', 'email': 'vinod@example.com'}
        ]

        for manager in managers:
            user = User(
                username=manager['username'].lower(),
                email=manager['email'],
                is_manager=True
            )
            user.set_password('LM123')
            db.session.add(user)

        db.session.commit()

        flash('Initial users created successfully. Line managers can login with their first name and password LM123', 'success')
        logger.info("Initial line manager users created")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating initial users: {str(e)}")
        flash(f'Error creating users: {str(e)}', 'danger')

    return redirect(url_for('auth.login'))