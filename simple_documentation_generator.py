"""
Simplified Documentation Generator for EMS Application

This script generates documentation without requiring the application to be running,
avoiding circular import issues.
"""
import os
import inspect
import importlib
from datetime import datetime
from xhtml2pdf import pisa
import ast

def safe_import(module_name):
    """Try to import a module safely without crashing on circular imports"""
    try:
        return importlib.import_module(module_name)
    except ImportError as e:
        print(f"Warning: Could not import {module_name}: {str(e)}")
        return None

def extract_docstrings(file_path):
    """Extract docstrings and function signatures from Python files"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    tree = ast.parse(content)
    module_doc = ast.get_docstring(tree)
    
    classes = []
    functions = []
    
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            class_info = {
                'name': node.name,
                'doc': ast.get_docstring(node) or "No documentation available.",
                'methods': []
            }
            
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    if item.name.startswith('_') and item.name != '__init__':
                        continue
                    
                    args = []
                    for arg in item.args.args:
                        args.append(arg.arg)
                    
                    method_info = {
                        'name': item.name,
                        'doc': ast.get_docstring(item) or "No documentation available.",
                        'signature': f"({', '.join(args)})"
                    }
                    class_info['methods'].append(method_info)
            
            classes.append(class_info)
        
        elif isinstance(node, ast.FunctionDef):
            args = []
            for arg in node.args.args:
                args.append(arg.arg)
                
            function_info = {
                'name': node.name,
                'doc': ast.get_docstring(node) or "No documentation available.",
                'signature': f"({', '.join(args)})"
            }
            functions.append(function_info)
    
    return {
        'doc': module_doc or "No documentation available.",
        'classes': classes,
        'functions': functions
    }

def generate_html_documentation():
    """Generate HTML documentation by parsing Python files"""
    # List of Python files to document
    files = [
        ('models.py', 'Data Models'),
        ('auth.py', 'Authentication Module'),
        ('employee.py', 'Employee Management Module'),
        ('feedback.py', 'Feedback System Module'),
        ('utils.py', 'Utility Functions')
    ]
    
    modules_data = []
    
    for file_name, description in files:
        if os.path.exists(file_name):
            module_data = extract_docstrings(file_name)
            module_data['name'] = file_name.replace('.py', '')
            module_data['description'] = description
            modules_data.append(module_data)
        else:
            print(f"Warning: File {file_name} not found")
    
    # Start building HTML
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>EMS Application Functionality Documentation</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1 {{ color: #2c3e50; text-align: center; }}
            h2 {{ color: #3498db; border-bottom: 1px solid #3498db; padding-bottom: 5px; }}
            h3 {{ color: #2980b9; }}
            h4 {{ color: #16a085; }}
            pre {{ background-color: #f8f9fa; padding: 10px; border-radius: 4px; }}
            .signature {{ font-family: monospace; background-color: #f0f0f0; padding: 3px; }}
            .module {{ margin-bottom: 30px; border: 1px solid #ddd; padding: 15px; border-radius: 5px; }}
            .class {{ margin-bottom: 20px; background-color: #f8f9fa; padding: 10px; border-radius: 4px; }}
            .method {{ margin-left: 20px; margin-bottom: 10px; }}
            .function {{ margin-bottom: 15px; background-color: #f8f9fa; padding: 10px; border-radius: 4px; }}
            .toc {{ background-color: #f8f9fa; padding: 10px; margin-bottom: 20px; }}
            .toc ul {{ padding-left: 20px; }}
            .screenshot {{ width: 95%; border: 1px solid #ddd; margin: 10px 0; }}
            .page-break {{ page-break-before: always; }}
            @page {{ size: A4; margin: 2cm; }}
        </style>
    </head>
    <body>
        <h1>Employee Management System Functionality Documentation</h1>
        <p style="text-align: center;">Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <div class="toc">
            <h2>Table of Contents</h2>
            <ul>
                <li><a href="#overview">Application Overview</a></li>
                <li><a href="#functionality">Key Functionalities</a>
                    <ul>
                        <li><a href="#auth">Authentication System</a></li>
                        <li><a href="#employee-management">Employee Management</a></li>
                        <li><a href="#feedback-system">Feedback System</a></li>
                        <li><a href="#import-export">Import/Export Functionality</a></li>
                    </ul>
                </li>
                <li><a href="#class-details">Module Details</a>
                    <ul>
    """
    
    # Add module links to TOC
    for module_data in modules_data:
        html += f'<li><a href="#{module_data["name"]}">{module_data["description"]}</a></li>\n'
    
    html += """
                    </ul>
                </li>
                <li><a href="#usage-guide">Usage Guide</a></li>
            </ul>
        </div>
        
        <!-- Application Overview -->
        <div class="page-break"></div>
        <h2 id="overview">Application Overview</h2>
        <p>
            The Employee Management System (EMS) is a comprehensive web application built with Flask and PostgreSQL
            that allows line managers to maintain employee details and provide feedback throughout the year.
            The system provides full CRUD operations for employee data management, feedback tracking, and reporting.
        </p>
        <p>
            The application is organized with a modular structure, separating concerns into different components:
            authentication, employee management, feedback system, and utility functions.
        </p>
        
        <!-- Key Functionalities with Screenshots -->
        <div class="page-break"></div>
        <h2 id="functionality">Key Functionalities</h2>
        
        <h3 id="auth">Authentication System</h3>
        <p>The authentication system handles user login, logout, and profile management with the following features:</p>
        <ul>
            <li>User login with username and password</li>
            <li>Role-based access control (manager vs. employee)</li>
            <li>Profile management</li>
            <li>Password security using bcrypt hashing</li>
        </ul>
        <p>Key Classes/Functions:</p>
        <ul>
            <li><code>User</code> model in models.py</li>
            <li><code>login()</code>, <code>logout()</code>, <code>profile()</code> functions in auth.py</li>
        </ul>
        <h4>Authentication Screenshots</h4>
        <p><strong>Login Page</strong></p>
        <div class="screenshot-placeholder">
            [Login Page Screenshot]
        </div>
        <p><strong>User Profile Page</strong></p>
        <div class="screenshot-placeholder">
            [Profile Page Screenshot]
        </div>
        
        <h3 id="employee-management">Employee Management</h3>
        <p>The employee management module handles all operations related to employee data:</p>
        <ul>
            <li>Dashboard overview of team and statistics</li>
            <li>Employee listing with sorting and filtering</li>
            <li>Employee details view</li>
            <li>Create, update, and delete employee records</li>
        </ul>
        <p>Key Classes/Functions:</p>
        <ul>
            <li><code>Employee</code> model in models.py</li>
            <li><code>dashboard()</code>, <code>employee_list()</code>, <code>create_employee()</code> functions in employee.py</li>
        </ul>
        <h4>Employee Management Screenshots</h4>
        <p><strong>Dashboard</strong></p>
        <div class="screenshot-placeholder">
            [Dashboard Screenshot]
        </div>
        <p><strong>Employee List</strong></p>
        <div class="screenshot-placeholder">
            [Employee List Screenshot]
        </div>
        <p><strong>Employee Details</strong></p>
        <div class="screenshot-placeholder">
            [Employee Details Screenshot]
        </div>
        
        <h3 id="feedback-system">Feedback System</h3>
        <p>The feedback system allows managers to provide structured feedback to their reportees:</p>
        <ul>
            <li>Create quarterly feedback with ratings and comments</li>
            <li>View feedback history for each employee</li>
            <li>Edit and delete feedback</li>
        </ul>
        <p>Key Classes/Functions:</p>
        <ul>
            <li><code>Feedback</code> model in models.py</li>
            <li><code>feedback_list()</code>, <code>create_feedback()</code> functions in feedback.py</li>
        </ul>
        <h4>Feedback System Screenshots</h4>
        <p><strong>Feedback List</strong></p>
        <div class="screenshot-placeholder">
            [Feedback List Screenshot]
        </div>
        <p><strong>Create Feedback</strong></p>
        <div class="screenshot-placeholder">
            [Create Feedback Screenshot]
        </div>
        
        <h3 id="import-export">Import/Export Functionality</h3>
        <p>The import/export module enables data exchange with Excel spreadsheets:</p>
        <ul>
            <li>Import employee data from Excel (manager_toolkit.xlsx)</li>
            <li>Export employee data to Excel format</li>
        </ul>
        <p>Key Classes/Functions:</p>
        <ul>
            <li><code>import_export()</code> function in employee.py</li>
            <li><code>export_employees_to_excel()</code> function in utils.py</li>
        </ul>
        <h4>Import/Export Screenshots</h4>
        <p><strong>Import/Export Interface</strong></p>
        <div class="screenshot-placeholder">
            [Import/Export Screenshot]
        </div>
        
        <!-- Module Details Section -->
        <div class="page-break"></div>
        <h2 id="class-details">Module Details</h2>
    """
    
    # Add module details
    for module_data in modules_data:
        html += f"""
        <div class="module page-break" id="{module_data['name']}">
            <h3>{module_data['name']}.py - {module_data['description']}</h3>
            <pre>{module_data['doc']}</pre>
            
            <h4>Classes:</h4>
        """
        
        if not module_data['classes']:
            html += "<p>No classes defined in this module.</p>"
        else:
            for class_data in module_data['classes']:
                html += f"""
                <div class="class">
                    <h4>{class_data['name']}</h4>
                    <pre>{class_data['doc']}</pre>
                    
                    <h5>Methods:</h5>
                """
                
                if not class_data['methods']:
                    html += "<p>No methods defined in this class.</p>"
                else:
                    for method in class_data['methods']:
                        html += f"""
                        <div class="method">
                            <h6>{method['name']}<span class="signature">{method['signature']}</span></h6>
                            <pre>{method['doc']}</pre>
                        </div>
                        """
                
                html += "</div>"
        
        html += """
            <h4>Functions:</h4>
        """
        
        if not module_data['functions']:
            html += "<p>No functions defined in this module.</p>"
        else:
            for function in module_data['functions']:
                html += f"""
                <div class="function">
                    <h5>{function['name']}<span class="signature">{function['signature']}</span></h5>
                    <pre>{function['doc']}</pre>
                </div>
                """
        
        html += "</div>"
    
    # Add Usage Guide
    html += """
        <div class="page-break"></div>
        <h2 id="usage-guide">Usage Guide</h2>
        
        <h3>Setup and Installation</h3>
        <ol>
            <li>Extract the ZIP file to a local directory</li>
            <li>Create a Python virtual environment: <code>python -m venv venv</code></li>
            <li>Activate the virtual environment:
                <ul>
                    <li>Windows: <code>venv\\Scripts\\activate</code></li>
                    <li>Linux/Mac: <code>source venv/bin/activate</code></li>
                </ul>
            </li>
            <li>Install dependencies: 
                <code>pip install flask flask-login flask-sqlalchemy gunicorn openpyxl pandas psycopg2-binary pygments sqlalchemy werkzeug xhtml2pdf</code>
            </li>
            <li>Configure database connection: <code>export DATABASE_URL="postgresql://username:password@localhost:5432/employee_management"</code></li>
            <li>Run the application: <code>gunicorn --bind 0.0.0.0:5000 main:app</code></li>
        </ol>
        
        <h3>Initial Setup</h3>
        <ol>
            <li>Navigate to <code>http://localhost:5000</code> in your browser</li>
            <li>Click "Initialize system" to create admin user</li>
            <li>Log in with username "admin" and password "admin123"</li>
            <li>Change the default password immediately</li>
        </ol>
        
        <h3>Using the Application</h3>
        <ol>
            <li>Import employee data via the Import/Export section</li>
            <li>Add, edit, or delete employees as needed</li>
            <li>Provide feedback to employees on a quarterly basis</li>
            <li>Use the dashboard to monitor employee performance</li>
        </ol>
    </body>
    </html>
    """
    
    return html

def create_pdf(html_content, output_path):
    """Convert HTML to PDF and save to file"""
    with open(output_path, "w+b") as pdf_file:
        pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)
    
    if pisa_status.err:
        return f"Error creating PDF: {pisa_status.err}"
    else:
        return f"PDF documentation created successfully at {output_path}"

if __name__ == "__main__":
    html_content = generate_html_documentation()
    result = create_pdf(html_content, "EMS_Functionality_Documentation.pdf")
    print(result)