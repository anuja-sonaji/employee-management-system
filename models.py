from datetime import datetime
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    """User model for authentication and authorization"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_manager = db.Column(db.Boolean, default=False)
    
    # Relationships
    employees_managed = db.relationship('Employee', backref='manager_user', lazy='dynamic',
                                        foreign_keys='Employee.manager_id')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Employee(db.Model):
    """Employee model to store employee details"""
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    joining_date = db.Column(db.Date, nullable=False)
    benzyl = db.Column(db.String(50), unique=True, nullable=False)  # Employee ID or username
    role = db.Column(db.String(100), nullable=False)
    skill = db.Column(db.String(100), nullable=False)
    team = db.Column(db.String(100), nullable=False)
    grade = db.Column(db.String(20), nullable=False)
    designation = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    
    # User account related to this employee (if any)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    user = db.relationship('User', foreign_keys=[user_id])
    
    # Manager relationship
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Relationships
    feedback_received = db.relationship('Feedback', backref='employee', lazy='dynamic',
                                        foreign_keys='Feedback.employee_id')
    
    def __repr__(self):
        return f'<Employee {self.full_name}>'


class Feedback(db.Model):
    """Feedback model to store manager feedback for employees"""
    __tablename__ = 'feedback'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    provided_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    provided_by = db.relationship('User', foreign_keys=[provided_by_id])
    
    rating = db.Column(db.Integer, nullable=False)  # e.g., 1-5 rating scale
    feedback_text = db.Column(db.Text, nullable=False)
    feedback_date = db.Column(db.DateTime, default=datetime.utcnow)
    month = db.Column(db.String(7), nullable=False)  # e.g., "2023-01"
    
    def __init__(self, **kwargs):
        super(Feedback, self).__init__(**kwargs)
        if not self.month:
            self.month = self.feedback_date.strftime('%Y-%m')
    
    def __repr__(self):
        return f'<Feedback for Employee #{self.employee_id} by {self.provided_by.username}>'
