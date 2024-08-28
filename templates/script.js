document.addEventListener('DOMContentLoaded', function () {
    const dataForm = document.getElementById('data-form');
    const chartContainer = document.getElementById('chart-container');

    dataForm.addEventListener('submit', function (e) {
        e.preventDefault();

        // Get form data
        const formData = new FormData(dataForm);

        // Send form data to the server for data processing
        fetch('/process_data', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            // Update chart container's data attributes
            chartContainer.setAttribute('data-chart-data', data.chartData);
            chartContainer.setAttribute('data-chart-layout', data.chartLayout);

            // Check if the chart data and layout attributes exist
            const chartData = chartContainer.getAttribute('data-chart-data');
            const chartLayout = chartContainer.getAttribute('data-chart-layout');

            if (chartData && chartLayout) {
                // Parse the JSON data and layout
                const parsedData = JSON.parse(chartData);
                const parsedLayout = JSON.parse(chartLayout);

                // Initialize and render the chart using the parsed data and layout
                Plotly.newPlot(chartContainer, parsedData, parsedLayout);
            } else {
                console.error('Chart data or layout attributes not found.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
