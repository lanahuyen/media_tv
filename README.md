
# Media Streaming Platforms Analysis and Visualization Project

## Overview
In recent years, the media streaming industry has experienced exponential growth, reshaping how viewers consume content. This project aims to explore this evolving landscape by conducting a detailed analysis of streaming platforms, viewer behavior, content quality, and pricing trends. Using datasets from various sources, including Netflix, IMDb, and historical pricing data, this project offers a comprehensive, narrative-driven exploration of the streaming market through an interactive web application.

The web application, built using Flask, employs advanced data visualization libraries such as Plotly to provide a user-friendly interface for exploring key trends and insights in the media streaming domain. The dashboard features a retro TV-themed design to engage users and enhance the interactive experience.

## Project Objectives
The primary objectives of this project are:
- Analyze the evolving media consumption patterns, emphasizing the shift from traditional TV to streaming services.
- Understand how different demographics engage with streaming platforms, exploring factors such as subscription preferences and viewing habits.
- Assess content quality across streaming platforms using metrics like IMDb ratings and genre diversity.
- Examine pricing models and revenue trends across major streaming platforms.
- Create an interactive web application that allows users to explore these insights through engaging visualizations.

## Features
1. **Comprehensive Data Integration**: Merges data from multiple sources, including Netflix and IMDb, to provide a holistic view of the streaming landscape.
2. **User-Driven Exploration**: Offers interactive elements such as dropdowns and dynamic charts, allowing users to explore data based on their interests.
3. **Multi-Faceted Analysis**: Covers various aspects of streaming services, including content quality, user demographics, subscription trends, and revenue analysis.
4. **Comparative Insights**: Presents a narrative that contrasts streaming platforms with traditional TV, highlighting the market shift.
5. **Retro TV-Themed UI**: Engaging user interface with a retro TV theme, including custom styling and a background that enhances the interactive experience.
6. **Interactive Movie Search**: Users can find the most popular movie based on genre and year, displaying the movie poster and title in a retro TV-styled display.

## Datasets
The project uses the following key datasets:
- **cleaned_NetflixTVShowsMovies.csv**: Contains detailed information on Netflix TV shows and movies, including genres, IMDb scores, and platform-specific data. This dataset is used to analyze content quality and genre distribution.
- **cleaned_NetflixUserbase.csv**: Provides insights into Netflix's user demographics, subscription types, and revenue. This dataset is essential for understanding user behavior and revenue patterns.
- **cleaned_AllServicesPriceHistory.csv**: Tracks the subscription price history of various streaming services over time, enabling an analysis of pricing trends and their impact on user behavior.
- **cleaned_IMDbMovies.csv**: Includes comprehensive information on a wide range of movies, including genres, IMDb ratings, and release years, allowing for cross-platform analysis of content quality.

## Data Processing and Cleaning
Data cleaning is a crucial step in this project. It involves handling missing values, normalizing formats (e.g., dates, text), and extracting relevant features. Key cleaning steps include:
- **Year Extraction**: Extracted four-digit years from the "Year" column in the IMDb dataset to ensure consistency for user search functionality.
- **Genre Filtering**: Implemented substring search for genres, allowing partial matches within the genre column.
- **Data Normalization**: Converted column names to lowercase and removed extra spaces for uniformity.
- **Handling Missing Data**: Imputed or excluded missing values to ensure the integrity of analysis results.

## Data Analysis
### Exploratory Data Analysis (EDA)
Initial EDA was conducted to understand the datasets' structures and identify key trends:
- **Genre Analysis**: Explored the diversity of genres available on different platforms and the popularity of each genre.
- **Subscription Trends**: Analyzed user subscription patterns and how they correlate with pricing and platform features.
- **Content Quality**: Assessed IMDb ratings across different platforms and genres to understand the quality and user reception of the content offered.

### Derived Metrics
- **Subscription Duration**: Calculated the duration of user subscriptions by computing the time between join dates and the last payment date.
- **Average Ratings**: Derived average IMDb ratings for various genres and platforms to identify content quality trends.
- **Revenue Metrics**: Summed monthly revenues to assess the financial performance of platforms across different regions.

## Visualizations
### Interactive Data Visualizations
The project employs Plotly to create a series of interactive visualizations, each serving a unique analytical purpose:
- **Trends in Selected Genre Over Time**: A dynamic chart showcasing the evolution of specific genres over time, providing insights into shifting viewer preferences.
- **IMDb Genre Distribution**: A Plotly bar chart illustrating the distribution of genres across the IMDb dataset, highlighting content diversity across platforms.
- **Platform-Specific Analysis**: Visualizations, including bar charts, that compare content quality (e.g., IMDb ratings) across different platforms.
- **Subscription Type Distribution**: A bar chart showing the breakdown of subscription types, offering insights into user preferences for basic, standard, or premium plans.
- **Revenue Analysis**: Line charts depicting the total monthly revenue by subscription type, revealing trends in platform adoption.
- **Subscription Price History**: A line chart tracking the historical price changes of various streaming services, providing context for market competition and pricing strategies.

### Movie Popularity Tool
- **Find the Most Popular Movie**: Allows users to select a genre and year to find the highest-rated movie using IMDb data. The result, including the movie's poster and title, is displayed on a retro TV-styled screen.

## Web Application
The web application serves as the project's interactive front end, enabling users to explore the data and insights dynamically. Built using Flask, the application comprises the following components:
- **Backend**: A Flask server that loads datasets, processes data, and serves visualizations through RESTful routes.
- **Frontend**: An HTML/CSS/JavaScript interface that dynamically displays visualizations based on user input.
- **Interactive Elements**: Dropdown menus, dynamic charts, and tooltips enhance user engagement, allowing for a tailored exploration of the streaming landscape.

### Flask Routes
- **/**: Main route that renders the homepage with various visualizations.
- **/update_data**: Processes user input to generate and return updated charts.
- **/get_most_popular**: Finds and returns the most popular movie based on the selected genre and year.

## Installation and Setup
### Prerequisites
- Python 3.x
- Flask, Pandas, Plotly, Flask-CORS, and other dependencies listed in `requirements.txt`

### Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/streaming-analysis-project.git
   cd streaming-analysis-project
   ```
2. **Create and Activate a Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Set Up Datasets**:
   - Ensure the datasets (`cleaned_NetflixTVShowsMovies.csv`, `cleaned_NetflixUserbase.csv`, `cleaned_AllServicesPriceHistory.csv`, and `cleaned_IMDbMovies.csv`) are located in the `data` directory.

5. **Run the Flask Application**:
   ```bash
   python app.py
   ```
6. **Access the Application**:
   - Open a web browser and navigate to `http://127.0.0.1:5000`.

## Usage Guide
Upon launching the application, users can explore various aspects of the streaming industry:
- **Genre Trends**: Use the interactive chart to view the evolution of selected genres over time.
- **Platform Comparisons**: Analyze IMDb ratings and content diversity across different platforms using dynamic visualizations.
- **User Demographics and Revenue**: Examine subscription type distribution and revenue patterns to gain insights into user behavior and market performance.
- **Find the Most Popular Movie**: Select a genre and year to find and display the highest-rated movie in a retro TV-style format.

## Future Enhancements
- **Real-Time Data Integration**: Incorporate real-time data feeds from streaming services and social media to provide up-to-date insights.
- **User Engagement Analysis**: Introduce metrics such as viewing time and content engagement to deepen the analysis of user behavior.
- **Predictive Analytics**: Apply machine learning models to predict future trends in viewer preferences, subscription growth, and revenue.

## Contributing
Contributions to this project are welcome. To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request for review.

## Acknowledgments
- **Data Sources**: Netflix, IMDb, Amazon Prime, Disney+, and Hulu datasets.


