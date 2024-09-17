#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pymongo import MongoClient
import pandas as pd

# Connect to MongoDB and access collections
client = MongoClient('mongodb://localhost:27017/')
db = client['media_consumption']
streaming_data = pd.DataFrame(list(db['streaming_content'].find()))
pricing_data = pd.DataFrame(list(db['pricing_data'].find()))


# In[3]:


print(streaming_data.columns)


# In[4]:


# Analyze genre popularity using the 'listed_in' column
genre_popularity = streaming_data['listed_in'].value_counts().reset_index()
genre_popularity.columns = ['genre', 'count']

# Display the genre popularity DataFrame
print(genre_popularity.head())


# In[6]:


print(pricing_data.columns)


# In[7]:


# Convert the 'date' column to datetime
pricing_data['date'] = pd.to_datetime(pricing_data['date'])

# Group by year and streaming service to analyze subscription trends over time
subscription_trends = pricing_data.groupby([pricing_data['date'].dt.year, 'streaming_service'])['subscription_price'].mean().reset_index()
subscription_trends.columns = ['year', 'streaming_service', 'average_subscription_price']

# Display the subscription trends DataFrame
print(subscription_trends.head())


# In[12]:


import altair as alt
import altair_viewer

# Example chart (replace with your specific chart code)
genre_chart = alt.Chart(genre_popularity).mark_bar().encode(
    x=alt.X('genre', sort='-y'),
    y='count',
    tooltip=['genre', 'count']
).properties(
    title='Genre Popularity on Streaming Platforms'
)


# In[13]:


genre_chart


# In[15]:


# Ensure 'date' is in datetime format
pricing_data['date'] = pd.to_datetime(pricing_data['date'])

# Create churn_analysis DataFrame (update column names as necessary)
churn_analysis = pricing_data.groupby(pricing_data['date'].dt.year)['subscription_price'].sum().reset_index()
churn_analysis.columns = ['date', 'subscribers']  # Adjust column names to fit your data


# In[16]:


churn_analysis


# In[31]:


print(churn_analysis.columns)


# In[32]:


# Ensure datetime format
churn_analysis['date'] = pd.to_datetime(churn_analysis['date'], format='%Y')


# In[33]:


# Create the Altair chart focusing on date and subscribers
subscription_trends = alt.Chart(churn_analysis).mark_line(point=True).encode(
    x=alt.X('date:T', title='Year'),
    y=alt.Y('subscribers:Q', title='Total Subscribers'),
    tooltip=['date:T', 'subscribers:Q']
).properties(
    title='Subscription Trends Over Time',
    width=600,
    height=400
).configure_axis(
    labelFontSize=12,
    titleFontSize=14
).configure_title(
    fontSize=16
)

# Display the chart
subscription_trends


# In[41]:


import pandas as pd

# Convert 'duration' to numeric (example: assuming 'duration' is in minutes)
# Modify this logic if 'duration' is in a different format (e.g., '2h 30m')
streaming_data['viewing_hours'] = pd.to_numeric(streaming_data['duration'], errors='coerce')

# Melt the platform columns to a single 'platform' column
platform_columns = ['netflix', 'hulu', 'prime_video', 'disney+']
melted_data = pd.melt(streaming_data, id_vars=['release_year', 'viewing_hours'], 
                      value_vars=platform_columns, var_name='platform', value_name='is_available')

# Filter out rows where the content is not available on the platform
melted_data = melted_data[melted_data['is_available'] == 1]

# Drop the 'is_available' column as it's no longer needed
melted_data = melted_data.drop(columns=['is_available'])


# In[44]:


print(melted_data.head())
print(melted_data.describe())


# In[45]:


print(melted_data['viewing_hours'].isna().sum())  # Check for NaN values
print(melted_data[melted_data['viewing_hours'] > 0].head())  # Check for positive values


# In[46]:


melted_data = melted_data[melted_data['viewing_hours'] > 0]


# In[48]:


# Increase the row limit to accommodate your data size
alt.data_transformers.disable_max_rows()

# Remove '_id' column if it exists
if '_id' in streaming_data.columns:
    streaming_data = streaming_data.drop(columns=['_id'])

viewing_patterns = alt.Chart(melted_data).mark_line().encode(
    x=alt.X('release_year:O', title='Year'),
    y=alt.Y('viewing_hours:Q', title='Viewing Hours'),
    color='platform:N',
    tooltip=['release_year:O', 'viewing_hours:Q', 'platform:N']
).properties(
    title='Viewing Patterns by Time and Platform',
    width=600,
    height=400
)

viewing_patterns


# In[50]:


# Load the streaming pricing data
pricing_data = pd.read_json('data/streaming_pricing_db.json')

# Convert date to datetime format
pricing_data['Date'] = pd.to_datetime(pricing_data['Date'], format='%m/%Y')

# Line chart for subscription pricing over time
pricing_chart = alt.Chart(pricing_data).mark_line().encode(
    x='Date:T',
    y='Subscription Price:Q',
    color='Streaming Service:N',
    tooltip=['Date', 'Streaming Service', 'Subscription Price']
).properties(
    title='Streaming Subscription Prices Over Time'
)

pricing_chart


# In[53]:


# Load the streaming content data
content_data = pd.read_json('data/streaming_content_db.json')

# Check column names to match the exact column names in the DataFrame
# Assuming column names are 'Netflix', 'Hulu', 'Prime Video', 'Disney+'
# If they are different in the DataFrame, adjust them accordingly

# Melt the DataFrame to analyze content availability
content_count = content_data.melt(id_vars=['Title'],  # You can use 'Title' or any other appropriate id_var
                                  value_vars=['Netflix', 'Hulu', 'Prime Video', 'Disney+'],
                                  var_name='platform', value_name='is_available')

# Filter out unavailable content (where is_available == 1)
content_count = content_count[content_count['is_available'] == 1]

# Group by content type and platform to count the number of titles
content_count = content_count.groupby(['platform']).size().reset_index(name='count')

# Bar chart for content availability
content_chart = alt.Chart(content_count).mark_bar().encode(
    x=alt.X('platform:N', title='Streaming Platform'),
    y=alt.Y('count:Q', title='Number of Titles'),
    tooltip=['platform', 'count']
).properties(
    title='Content Availability by Streaming Platform'
)

content_chart


# In[55]:


# Load the cable TV data
cable_data = pd.read_json('data/cabel_tv_db.json')

# Convert 'Year' to datetime format
cable_data['Year'] = pd.to_datetime(cable_data['Year'], format='%Y')

# Add a dummy 'Cost' column for illustration purposes
# Since the data doesn't have a cost column, you need to add relevant data if available
cable_data['Cost'] = [50 + (i * 2) for i in range(len(cable_data))]  # Example cost values

# Line chart for cable TV costs
cable_cost_chart = alt.Chart(cable_data).mark_line().encode(
    x='Year:T',
    y='Cost:Q',
    color=alt.value('orange'),
    tooltip=['Year', 'Cost']
).properties(
    title='Cable TV Subscription Costs Over Time'
)

cable_cost_chart


# In[56]:


# Count new titles per year by platform
engagement_data = streaming_data.melt(id_vars=['release_year'], value_vars=['netflix', 'hulu', 'prime_video', 'disney+'],
                                      var_name='platform', value_name='is_available')
engagement_data = engagement_data[engagement_data['is_available'] == 1]
engagement_data = engagement_data.groupby(['release_year', 'platform']).size().reset_index(name='new_titles')

# Line chart for user engagement and content trends
engagement_chart = alt.Chart(engagement_data).mark_line().encode(
    x=alt.X('release_year:O', title='Year'),
    y=alt.Y('new_titles:Q', title='Number of New Titles'),
    color='platform:N',
    tooltip=['release_year', 'new_titles', 'platform']
).properties(
    title='New Content Additions Over Time by Platform'
)

engagement_chart


# In[59]:


# Check columns again to identify an appropriate metric
print(pricing_data.columns)
print(streaming_data.columns)

# Merge the data on 'Date'
combined_data = pd.merge(pricing_data, streaming_data, on='Date', how='inner')

# If there's no 'subscribers' column, you might want to use another relevant column like 'Subscription Price' or any other metric
# Here's an example using 'Subscription Price' as a comparison for illustration purposes
# Calculate the ratio using available columns
combined_data['price_per_viewing_hour'] = combined_data['Subscription Price'] / combined_data['viewing_hours']

# Scatter plot for viewing hours vs subscription costs
scatter_chart = alt.Chart(combined_data).mark_circle().encode(
    x=alt.X('Subscription Price:Q', title='Subscription Price'),
    y=alt.Y('price_per_viewing_hour:Q', title='Price per Viewing Hour'),
    color='Streaming Service:N',
    tooltip=['Subscription Price', 'price_per_viewing_hour', 'Streaming Service']
).properties(
    title='Price per Viewing Hour vs Subscription Costs'
)

scatter_chart

