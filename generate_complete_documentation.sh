#!/bin/bash

# Fix template issues
echo "Fixing template issues..."
sed -i 's/{% if "employee_list" in request.endpoint %}/{% if request.endpoint and "employee_list" in request.endpoint %}/g' templates/base.html
sed -i 's/{% if "feedback" in request.endpoint %}/{% if request.endpoint and "feedback" in request.endpoint %}/g' templates/base.html
sed -i 's/{% if "import_export" in request.endpoint %}/{% if request.endpoint and "import_export" in request.endpoint %}/g' templates/base.html
sed -i 's/{% if request.endpoint == "employee.dashboard" %}/{% if request.endpoint and request.endpoint == "employee.dashboard" %}/g' templates/base.html

# Take screenshots of key pages (requires a running application)
echo "Taking screenshots (this would normally capture the application UI)..."
echo "Note: Real screenshots require a browser automation tool like Selenium"

# Create placeholder screenshots directory
mkdir -p screenshots

# Generate detailed documentation PDF
echo "Generating documentation..."
python create_functionality_docs.py

# Generate code-level documentation
echo "Generating code documentation..."
python generate_documentation.py

echo "Documentation generation complete!"
echo "Files created:"
echo "- EMS_Functionality_Documentation.pdf (functionality details with class documentation)"
echo "- EMS_Documentation.pdf (complete code listing)"