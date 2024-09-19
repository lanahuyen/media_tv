from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pandas as pd
import plotly.express as px
import plotly
import json

# Create the Flask app instance
app = Flask(__name__)
CORS(app)  # Enable CORS if needed

# Load datasets
price_history_df = pd.read_csv('data/cleaned_AllServicesPriceHistory.csv')
netflix_userbase_df = pd.read_csv('data/cleaned_NetflixUserbase.csv')

# Load and clean the IMDb movies dataset
imdb_movies_df = pd.read_csv('data/cleaned_IMDbMovies.csv')

# Clean the "Year" column: Extract year as an integer, handle NaN values
imdb_movies_df['Year'] = imdb_movies_df['Year'].astype(str).str.extract(r'(\d{4})')
imdb_movies_df = imdb_movies_df.dropna(subset=['Year'])  # Drop rows where "Year" is NaN
imdb_movies_df['Year'] = imdb_movies_df['Year'].astype(int)  # Convert "Year" to integer

@app.route('/')
def index():
    # List of genres to use in the dropdown
    genre_list = [
        'Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 
        'Documentary', 'Drama', 'Family', 'Fantasy', 'Film-Noir', 'History', 
        'Horror', 'Music', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 
        'Sport', 'Thriller', 'War', 'Western'
    ]
    return render_template('index.html', genres=genre_list)

@app.route('/update_data', methods=['POST'])
def update_data():
    try:
        # Get filter criteria from the form
        data = request.json
        gender = data.get('gender', 'All')
        chart_type = data.get('chart_type', 'subscription')  # Updated: Default to 'subscription'

        # Filter the Netflix user base data based on gender only
        filtered_data = netflix_userbase_df

        if gender != 'All':
            filtered_data = filtered_data[filtered_data['Gender'] == gender]

        # Create the desired chart based on the chart type
        if chart_type == 'subscription':
            # Group and count the data for the bar chart
            grouped_data = filtered_data.groupby(['Subscription Type', 'Gender']).size().reset_index(name='Count')

            # Create Plotly bar figure without extra details
            if grouped_data.empty:
                fig = px.bar(title='No data available for the selected criteria')
            else:
                fig = px.bar(grouped_data, x='Subscription Type', y='Count', color='Gender',
                             title='Subscription Data by Gender')
        
        elif chart_type == 'monthly':
            # Prepare data for the line chart (e.g., Monthly Revenue over Time)
            if 'Join Date' in filtered_data.columns and 'Monthly Revenue' in filtered_data.columns:
                filtered_data['Join Date'] = pd.to_datetime(filtered_data['Join Date'])
                revenue_data = filtered_data.groupby(['Join Date', 'Subscription Type']).sum().reset_index()

                # Create Plotly line figure
                if revenue_data.empty:
                    fig = px.line(title='No data available for the selected criteria')
                else:
                    fig = px.line(revenue_data, x='Join Date', y='Monthly Revenue', color='Subscription Type',
                                  title='Monthly Revenue Over Time')
            else:
                fig = px.line(title='Required columns are missing for the line chart')

        elif chart_type == 'device':
            # Prepare data for the pie chart (e.g., Device distribution)
            if 'Device' in filtered_data.columns:
                device_data = filtered_data.groupby('Device').size().reset_index(name='Count')

                # Create Plotly pie figure
                if device_data.empty:
                    fig = px.pie(title='No data available for the selected criteria')
                else:
                    fig = px.pie(device_data, values='Count', names='Device', title='Device Distribution')
            else:
                fig = px.pie(title='Required columns are missing for the pie chart')

        # Serialize the figure to JSON
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return jsonify({'graphJSON': graphJSON})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/get_most_popular', methods=['POST'])
def get_most_popular():
    try:
        # Get filter criteria from the form
        genre = request.json.get('genre')
        year = request.json.get('year')

        # Ensure year is an integer
        year = int(year)

        # Filter the IMDb movies data where the 'Genre' column contains the selected genre and the 'Year' matches
        filtered_movies = imdb_movies_df[
            (imdb_movies_df['Genre'].str.contains(genre, case=False, na=False)) & 
            (imdb_movies_df['Year'] == year)
        ]

        # Find the movie with the highest Metascore
        if not filtered_movies.empty:
            most_popular = filtered_movies.loc[filtered_movies['Metascore'].idxmax()]
            result = {
                'title': most_popular['Title'],
                'poster': most_popular['Poster']
            }
        else:
            result = {'error': 'No movies found for the selected criteria.'}

        return jsonify(result)

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)