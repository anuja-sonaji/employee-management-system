document.addEventListener('DOMContentLoaded', function() {
    // Initialize DataTables for employee list
    const employeeTable = document.getElementById('employeeTable');
    if (employeeTable) {
        new DataTable('#employeeTable', {
            responsive: true,
            dom: '<"row"<"col-md-6"l><"col-md-6"f>>rt<"row"<"col-md-6"i><"col-md-6"p>>B',
            buttons: [
                'copy', 'csv', 'excel', 'pdf', 'print'
            ],
            order: [[0, 'asc']], // Sort by name by default
            pageLength: 10,
            language: {
                search: "Filter:",
                lengthMenu: "Show _MENU_ employees per page",
                info: "Showing _START_ to _END_ of _TOTAL_ employees",
                infoEmpty: "Showing 0 to 0 of 0 employees",
                infoFiltered: "(filtered from _MAX_ total employees)"
            },
            initComplete: function() {
                // Connect the global search with DataTables search
                const dataTable = this;
                $('#searchInput').on('keyup', function() {
                    dataTable.api().search($(this).val()).draw();
                });
            }
        });
    }

    // Initialize DataTables for feedback list
    const feedbackTable = document.getElementById('feedbackTable');
    if (feedbackTable) {
        new DataTable('#feedbackTable', {
            responsive: true,
            dom: '<"row"<"col-md-6"l><"col-md-6"f>>rt<"row"<"col-md-6"i><"col-md-6"p>>',
            order: [[3, 'desc']], // Sort by date by default
            pageLength: 10,
            language: {
                search: "Filter:",
                lengthMenu: "Show _MENU_ feedback entries per page",
                info: "Showing _START_ to _END_ of _TOTAL_ feedback entries",
                infoEmpty: "Showing 0 to 0 of 0 feedback entries",
                infoFiltered: "(filtered from _MAX_ total feedback entries)"
            },
            initComplete: function() {
                // Connect the global search with DataTables search
                const dataTable = this;
                $('#searchInput').on('keyup', function() {
                    dataTable.api().search($(this).val()).draw();
                });
            }
        });
    }

    // For dashboard stats, initialize simple charts
    const teamSkillsChart = document.getElementById('teamSkillsChart');
    if (teamSkillsChart) {
        // Extract data from the page
        const labels = [];
        const data = [];
        
        document.querySelectorAll('.skill-stat').forEach(stat => {
            labels.push(stat.getAttribute('data-skill'));
            data.push(parseInt(stat.getAttribute('data-count')));
        });
        
        // Create chart
        new Chart(teamSkillsChart, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: [
                        '#4e73df', '#1cc88a', '#36b9cc', '#f6c23e', '#e74a3b',
                        '#5a5c69', '#858796', '#2e59d9', '#17a673', '#2c9faf'
                    ],
                    hoverBackgroundColor: [
                        '#2e59d9', '#17a673', '#2c9faf', '#f6c23e', '#e74a3b',
                        '#5a5c69', '#858796', '#2e59d9', '#17a673', '#2c9faf'
                    ],
                    hoverBorderColor: "rgba(234, 236, 244, 1)",
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                    },
                    title: {
                        display: true,
                        text: 'Team Skills Distribution'
                    }
                }
            }
        });
    }

    // Feedback trends chart (for managers)
    const feedbackTrendsChart = document.getElementById('feedbackTrendsChart');
    if (feedbackTrendsChart) {
        // Extract data from the page (this would be populated by the backend)
        const quarters = [];
        const avgRatings = [];
        
        document.querySelectorAll('.feedback-trend').forEach(trend => {
            quarters.push(trend.getAttribute('data-quarter'));
            avgRatings.push(parseFloat(trend.getAttribute('data-avg-rating')));
        });
        
        // Create chart
        new Chart(feedbackTrendsChart, {
            type: 'line',
            data: {
                labels: quarters,
                datasets: [{
                    label: 'Average Rating',
                    data: avgRatings,
                    lineTension: 0.3,
                    backgroundColor: "rgba(78, 115, 223, 0.05)",
                    borderColor: "rgba(78, 115, 223, 1)",
                    pointRadius: 3,
                    pointBackgroundColor: "rgba(78, 115, 223, 1)",
                    pointBorderColor: "rgba(78, 115, 223, 1)",
                    pointHoverRadius: 5,
                    pointHoverBackgroundColor: "rgba(78, 115, 223, 1)",
                    pointHoverBorderColor: "rgba(78, 115, 223, 1)",
                    pointHitRadius: 10,
                    pointBorderWidth: 2,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        min: 0,
                        max: 5,
                        ticks: {
                            stepSize: 1
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: 'Feedback Rating Trends by Quarter'
                    }
                }
            }
        });
    }
});
