// scripts.js
document.addEventListener('DOMContentLoaded', function() {
    // Fetch and render the Altair chart (existing chart)
    fetch('/get-plot/interactive-genres')
        .then(response => response.json())
        .then(chartSpec => {
            // Use Vega-Embed to render the chart
            vegaEmbed('#genre-chart', chartSpec);
        })
        .catch(error => console.error('Error loading the chart:', error));

    // Fetch and render the IMDb Genres Plot (New Plot using Plotly)
    fetch('/get-plot/imdb-genres')
        .then(response => response.json())
        .then(data => {
            Plotly.newPlot('imdb-genres-plot-container', data.data, data.layout);
        })
        .catch(error => console.error('Error loading the IMDb genres plot:', error));
    
    // More fetch calls can be added here for additional plots
});