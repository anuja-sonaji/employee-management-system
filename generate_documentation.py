import os
import glob
from pygments import highlight
from pygments.lexers import get_lexer_for_filename, PythonLexer
from pygments.formatters import HtmlFormatter
from xhtml2pdf import pisa
import datetime

def get_file_content(file_path):
    """Read file content with proper encoding handling"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as file:
            return file.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def highlight_code(code, file_path):
    """Highlight code based on file extension"""
    try:
        if file_path.endswith('.py'):
            lexer = PythonLexer()
        else:
            lexer = get_lexer_for_filename(file_path)
        return highlight(code, lexer, HtmlFormatter(full=False))
    except Exception:
        # If highlighting fails, return the code as is
        return f"<pre>{code}</pre>"

def create_pdf_documentation():
    """Generate PDF documentation with all code files"""
    # List of directories to include
    directories = [
        '.', 'templates', 'static/css', 'static/js'
    ]
    
    # File extensions to include
    extensions = [
        '*.py', '*.html', '*.css', '*.js'
    ]
    
    # Files to exclude
    exclude_files = [
        '.git', '.upm', '__pycache__', '.replit', 'replit.nix',
        'pyproject.toml', 'poetry.lock', 'uv.lock', 'generate_documentation.py'
    ]
    
    # Collect all files
    all_files = []
    for directory in directories:
        if os.path.exists(directory):
            for ext in extensions:
                pattern = os.path.join(directory, '**', ext)
                files = glob.glob(pattern, recursive=True)
                all_files.extend(files)
    
    # Filter excluded files
    filtered_files = []
    for file_path in all_files:
        exclude = False
        for excluded in exclude_files:
            if excluded in file_path:
                exclude = True
                break
        if not exclude:
            filtered_files.append(file_path)
    
    # Sort files by type and name
    filtered_files.sort(key=lambda x: (os.path.splitext(x)[1], x))
    
    # Create HTML for PDF
    css = HtmlFormatter().get_style_defs('.highlight')
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>EMS Application Documentation</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1 {{ color: #2c3e50; }}
            h2 {{ color: #3498db; border-bottom: 1px solid #3498db; padding-bottom: 5px; }}
            h3 {{ color: #2980b9; }}
            .file-path {{ background-color: #f7f7f7; padding: 5px; border-left: 3px solid #3498db; }}
            .toc {{ background-color: #f8f9fa; padding: 10px; margin-bottom: 20px; }}
            .toc h2 {{ margin-top: 0; }}
            .toc ul {{ padding-left: 20px; }}
            pre {{ white-space: pre-wrap; }}
            code {{ font-family: Consolas, Monaco, 'Andale Mono', monospace; }}
            {css}
            @page {{ size: A4; margin: 2cm; }}
            .page-break {{ page-break-before: always; }}
        </style>
    </head>
    <body>
        <h1>Employee Management System Documentation</h1>
        <p>Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <div class="toc">
            <h2>Table of Contents</h2>
            <ul>
    """
    
    # Add TOC entries
    for file_path in filtered_files:
        html += f'<li><a href="#{file_path.replace("/", "_").replace(".", "_")}">{file_path}</a></li>\n'
    
    html += """
            </ul>
        </div>
        
        <h2>File Listing</h2>
    """
    
    # Add each file content
    for file_path in filtered_files:
        content = get_file_content(file_path)
        highlighted_content = highlight_code(content, file_path)
        file_id = file_path.replace("/", "_").replace(".", "_")
        
        html += f"""
        <div class="page-break"></div>
        <h3 id="{file_id}">{file_path}</h3>
        <div class="file-path">{file_path}</div>
        <div class="code">
            {highlighted_content}
        </div>
        """
    
    html += """
    </body>
    </html>
    """
    
    # Convert HTML to PDF
    output_path = "EMS_Documentation.pdf"
    with open(output_path, "w+b") as pdf_file:
        pisa_status = pisa.CreatePDF(html, dest=pdf_file)
    
    if pisa_status.err:
        return f"Error creating PDF: {pisa_status.err}"
    else:
        return f"PDF documentation created successfully at {output_path}"

if __name__ == "__main__":
    print(create_pdf_documentation())