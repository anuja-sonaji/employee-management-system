# Employee Management System (EMS)

A comprehensive web application built with Flask and PostgreSQL that allows line managers to maintain employee details and provide feedback throughout the year.

## Features

### Authentication System
- User login with username/password
- Role-based access control (manager vs. employee)
- Profile management with secure password storage

### Employee Management
- Dashboard with team overview and statistics
- Employee listing with sorting and filtering
- Detailed employee profiles
- CRUD operations for employee records

### Feedback System
- Quarterly feedback tracking
- Rating system with comments
- Feedback history for each employee
- Performance tracking over time

### Data Import/Export
- Import employee data from Excel
- Export employee data to Excel
- Data validation and error handling

## Technology Stack

- **Backend**: Python Flask
- **Database**: PostgreSQL (SQLite fallback)
- **ORM**: SQLAlchemy
- **Authentication**: Flask-Login
- **Frontend**: Bootstrap 5 with Dark Theme
- **Data Tables**: jQuery DataTables
- **Charts**: Chart.js
- **Excel Processing**: Pandas, Openpyxl
- **Documentation**: xhtml2pdf, Pygments

## Getting Started

### Prerequisites
- Python 3.6+
- PostgreSQL database

### Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install flask flask-login flask-sqlalchemy gunicorn openpyxl pandas psycopg2-binary pygments sqlalchemy werkzeug xhtml2pdf
   ```
3. Set environment variables:
   ```
   export DATABASE_URL="postgresql://username:password@localhost:5432/employee_management"
   ```
4. Run the application:
   ```
   gunicorn --bind 0.0.0.0:5000 main:app
   ```

### Initial Setup

1. Navigate to `http://localhost:5000` in your browser
2. Click "Initialize system" to create admin user
3. Log in with username `admin` and password `admin123`
4. Change the default password immediately
5. Import employee data from the Excel spreadsheet

## Documentation

The system includes built-in documentation generators:

1. **Code Documentation**:
   ```
   python generate_documentation.py
   ```
   This creates a PDF with the complete source code documentation.

2. **Functionality Documentation**:
   ```
   python simple_documentation_generator.py
   ```
   This creates a PDF with functional documentation, class descriptions, and usage guides.

## Data Import Format

The system imports employee data from an Excel file with the following columns:
- Full Name
- Benzyl (Employee ID)
- Role
- Skill
- Team
- Manager Name
- Grade
- Designation
- Location
- Joining Date

## Security Features

- Password hashing using Werkzeug security
- Role-based access control
- Session management with Flask-Login
- CSRF protection
- Input validation

## Project Structure

- `app.py`: Application initialization and configuration
- `main.py`: Main entry point
- `models.py`: SQLAlchemy data models
- `auth.py`: Authentication routes and logic
- `employee.py`: Employee management functionality
- `feedback.py`: Feedback system routes and functions
- `utils.py`: Utility functions
- `docs.py`: Documentation generation endpoints
- `static/`: Static assets (CSS, JS)
- `templates/`: Jinja2 HTML templates
- `generate_documentation.py`: Code documentation generator
- `simple_documentation_generator.py`: Functional documentation generator

## License

This project is licensed under the MIT License - see the LICENSE file for details.