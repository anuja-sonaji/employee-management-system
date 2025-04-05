from flask import Blueprint, send_file, flash, redirect, url_for
from flask_login import login_required, current_user
import os
from utils import require_manager
import subprocess

# Create a Blueprint for documentation
docs_bp = Blueprint('docs', __name__)

@docs_bp.route('/documentation')
@login_required
@require_manager
def generate_and_download_docs():
    """Generate and download the documentation PDF"""
    try:
        # Run the documentation generator script
        result = subprocess.run(['python', 'generate_documentation.py'], 
                                capture_output=True, text=True, check=True)
        
        # Check if the file was created
        if os.path.exists('EMS_Documentation.pdf'):
            return send_file('EMS_Documentation.pdf', as_attachment=True)
        else:
            flash('Failed to generate documentation: ' + result.stdout, 'danger')
            return redirect(url_for('employee.dashboard'))
            
    except subprocess.CalledProcessError as e:
        flash(f'Error generating documentation: {e.stderr}', 'danger')
        return redirect(url_for('employee.dashboard'))
    except Exception as e:
        flash(f'Unexpected error: {str(e)}', 'danger')
        return redirect(url_for('employee.dashboard'))