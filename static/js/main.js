// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Handle flash message dismissal
    setTimeout(function() {
        let alerts = document.querySelectorAll('.alert-auto-dismiss');
        alerts.forEach(function(alert) {
            let bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Confirm delete operations
    document.querySelectorAll('.confirm-delete').forEach(function(button) {
        button.addEventListener('click', function(event) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                event.preventDefault();
            }
        });
    });

    // Star rating system for feedback
    const ratingInputs = document.querySelectorAll('.rating-input');
    const ratingStars = document.querySelectorAll('.rating-star');

    if (ratingStars.length > 0) {
        ratingStars.forEach(star => {
            star.addEventListener('click', function() {
                const value = this.getAttribute('data-value');
                document.getElementById('rating').value = value;
                
                // Update star display
                ratingStars.forEach(s => {
                    const starValue = s.getAttribute('data-value');
                    if (starValue <= value) {
                        s.classList.add('rated');
                    } else {
                        s.classList.remove('rated');
                    }
                });
            });
        });
    }

    // Toggle side navigation for mobile
    const sidebarToggle = document.getElementById('sidebarToggle');
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            document.body.classList.toggle('sidebar-toggled');
            document.querySelector('.sidebar').classList.toggle('toggled');
        });
    }

    // Handle search functionality
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keyup', function() {
            const searchTerm = this.value.toLowerCase();
            
            // Find if we have a DataTable initialized
            if ($.fn.dataTable.isDataTable('#employeeTable')) {
                // Use DataTables search if available
                $('#employeeTable').DataTable().search(searchTerm).draw();
            } else if ($.fn.dataTable.isDataTable('#feedbackTable')) {
                // Use DataTables search if available
                $('#feedbackTable').DataTable().search(searchTerm).draw();
            } else {
                // Fallback to manual search if no DataTable
                const table = document.querySelector('table');
                if (table) {
                    const rows = table.querySelectorAll('tbody tr');
                    
                    rows.forEach(row => {
                        const text = row.textContent.toLowerCase();
                        if(text.includes(searchTerm)) {
                            row.style.display = '';
                        } else {
                            row.style.display = 'none';
                        }
                    });
                }
            }
        });
    }
});
