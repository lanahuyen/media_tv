from flask import Flask, render_template, jsonify
import pandas as pd
import plotly.express as px
import json
import plotly

app = Flask(__name__)

# Load datasets
netflix_tv_df = pd.read_csv('data/cleaned_NetflixTVShowsMovies.csv')
netflix_userbase_df = pd.read_csv('data/cleaned_NetflixUserbase.csv')
price_history_df = pd.read_csv('data/all_services_price_history.csv')
imdb_df = pd.read_csv('data/cleaned_IMDbMovies.csv')

# Basic Data Processing
# Convert relevant columns to lowercase for consistency if needed
netflix_tv_df['Platform'] = netflix_tv_df['Platform'].str.lower()

# Convert date columns
price_history_df['Date'] = pd.to_datetime(price_history_df['Date'], format='%m/%Y', errors='coerce')

# Ensure 'Genre' column exists in the IMDb data
if 'Genre' not in imdb_df.columns:
    raise KeyError("The 'Genre' column is missing from the IMDb dataset")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-plot/interactive-genres')
def get_interactive_genres_plot():
    # Example: Trends in Selected Genre Over Time (Altair chart)
    # You need to replace this example with the actual implementation of your Altair chart
    # Replace the following code with the actual logic used in your project to create the Altair chart spec
    chart_spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": "A simple bar chart with embedded data.",
        "data": {
            "values": [
                {"a": "A", "b": 28}, {"a": "B", "b": 55}, {"a": "C", "b": 43},
                {"a": "D", "b": 91}, {"a": "E", "b": 81}, {"a": "F", "b": 53},
                {"a": "G", "b": 19}, {"a": "H", "b": 87}, {"a": "I", "b": 52}
            ]
        },
        "mark": "bar",
        "encoding": {
            "x": {"field": "a", "type": "nominal"},
            "y": {"field": "b", "type": "quantitative"}
        }
    }
    
    return jsonify(chart_spec)

@app.route('/get-plot/imdb-genres')
def get_imdb_genres_plot():
    # Visualization: IMDb Genre Distribution
    genre_counts = imdb_df['Genre'].str.split(',').explode().value_counts().reset_index()
    genre_counts.columns = ['Genre', 'Count']
    fig = px.bar(genre_counts, x='Genre', y='Count', title='Distribution of IMDb Genres')
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route('/get-plot/platform/<platform>')
def get_platform_plot(platform):
    # Visualization: IMDb Ratings by Genre for the Selected Platform
    filtered_data = netflix_tv_df[netflix_tv_df['Platform'] == platform]
    fig = px.bar(filtered_data, x='Genre', y='imdb_score', title=f'IMDb Ratings for {platform.capitalize()}')

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route('/get-plot/userbase')
def get_userbase_plot():
    # Visualization: Subscription Type Distribution
    subscription_counts = netflix_userbase_df['Subscription Type'].value_counts().reset_index()
    subscription_counts.columns = ['Subscription Type', 'Count']
    fig = px.pie(subscription_counts, values='Count', names='Subscription Type', title='Subscription Type Distribution')
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route('/get-plot/revenue')
def get_revenue_plot():
    # Visualization: Total Monthly Revenue by Country
    revenue_by_country = netflix_userbase_df.groupby('Country')['Monthly Revenue'].sum().reset_index()
    fig = px.bar(revenue_by_country, x='Country', y='Monthly Revenue', title='Total Monthly Revenue by Country')

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route('/get-plot/price-history')
def get_price_history_plot():
    # Visualization: Subscription Price History
    fig = px.line(price_history_df, x='Date', y='Subscription Price', color='Streaming Service', title='Subscription Price History')

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

if __name__ == '__main__':
    app.run(debug=True)