import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter
import re
import plotly.express as px

#st.set_page_config(layout="wide")

# Load the data
tweets_df = pd.read_csv('tweetsdata.csv')

# Strip whitespace from column names
tweets_df.columns = tweets_df.columns.str.strip()

# Preprocess data
tweets_df['text'] = tweets_df['text'].fillna('').astype(str)

# Extract hashtags
def extract_hashtags_safe(text):
    try:
        return re.findall(r'#\w+', text.lower())
    except AttributeError:
        return []
tweets_df['hashtags'] = tweets_df['text'].apply(extract_hashtags_safe)

# Categorize sentiment
def categorize_sentiment(score):
    if score > 0:
        return 'Positive'
    elif score < 0:
        return 'Negative'
    else:
        return 'Neutral'
tweets_df['SentimentCategory'] = tweets_df['Sentiment'].apply(categorize_sentiment)

# Dashboard Layout
st.title("Twitter Analytics Dashboard")

# Metrics Section
st.header("Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Tweets", len(tweets_df))
col2.metric("Contributors", tweets_df['UserID'].nunique())
col3.metric("Countries", tweets_df['Country'].nunique())
col4.metric("Likes", int(tweets_df['Likes'].sum()))


col5, col6, col7, col8 = st.columns(4)
col5.metric("Max Reach", int(tweets_df['Reach'].max()))
col6.metric("Retweets", int(tweets_df['RetweetCount'].max()))
#col7.metric("")
#col8.metric("")

# Top 15 Twitter Trends (Hashtags)
st.header("Top 15 Twitter Trends (Hashtags)")
all_hashtags = [h for sublist in tweets_df['hashtags'] for h in sublist]
top_hashtags = Counter(all_hashtags).most_common(15)
hashtags_df = pd.DataFrame(top_hashtags, columns=['Hashtag', 'Count'])
st.bar_chart(hashtags_df.set_index('Hashtag'))

# Tweets on Timeline
st.header("Tweets on Timeline")
fig, ax = plt.subplots(figsize=(10, 6))
tweets_df['Hour'].value_counts().sort_index().plot(kind='bar', ax=ax, color='orange')
plt.title("Tweet Activity by Hour")
plt.xlabel("Hour of Day")
plt.ylabel("Tweet Count")
st.pyplot(fig)


# Word Cloud
st.header("Hashtags Cloud")

# Prepare data for the word cloud
all_hashtags = [h for sublist in tweets_df['hashtags'] for h in sublist]  # Flatten the list of hashtags
hashtag_counts = Counter(all_hashtags)  # Count the occurrences of each hashtag

# Generate the word cloud
wordcloud = WordCloud(
    width=800, 
    height=400, 
    background_color='white', 
    colormap='tab10',  # Use a colorful colormap
    max_words=200  # Limit the number of words
).generate_from_frequencies(hashtag_counts)

# Plot the word cloud
fig, ax = plt.subplots(figsize=(10, 6))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis('off')  # Remove axes
st.pyplot(fig)




# Twitter Distribution by Country on World Map
st.header("Gender Distribution by Country (World Map)")

# Aggregate Tweets counts by country
gender_country = tweets_df.groupby(['Country', 'Gender']).size().unstack(fill_value=0).reset_index()
gender_country['Total'] = gender_country.select_dtypes(include='number').sum(axis=1)  # Sum only numeric columns

# Create a choropleth map
fig = px.choropleth(
    gender_country,
    locations="Country",  # Column with country names
    locationmode="country names",  # Match country names
    color="Total",  # Color by total tweet count
    hover_name="Country",  # Display country name on hover
    title="Tweets Distribution by Country",
    color_continuous_scale=["#FF9999", "#66B2FF", "#99FF99"],
    #color_continuous_scale=px.colors.sequential.Viridis #Plasma
    
    width=900,  # Set the width of the map
    height=700   # Set the height of the map
)

# Display the map
st.plotly_chart(fig)


# Sentiment Analysis Pie Chart
st.header("Sentiment Analysis")
sentiment_counts = tweets_df['SentimentCategory'].value_counts()

custom_colors = ['#FF9999', '#66B2FF', '#99FF99']

fig, ax = plt.subplots(figsize=(3, 3))
ax.pie(sentiment_counts.values, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=140, colors=custom_colors) #colors=sns.color_palette("pastel"))
ax.set_title("Sentiment Distribution")
st.pyplot(fig)



# Gender Distribution by Country
#st.header("Gender Distribution by Country")
#gender_country = tweets_df.groupby(['Country', 'Gender']).size().unstack(fill_value=0)
#fig, ax = plt.subplots(figsize=(10, 6))
#gender_country.plot(kind='bar', stacked=True, ax=ax, color=['skyblue', 'pink'])
#plt.title("Gender Distribution by Country")
#plt.xlabel("Country")
#plt.ylabel("Tweet Count")
#st.pyplot(fig)


# Gender Distribution by Country
st.header("Gender Distribution by Country")

# Aggregate and sort by total tweet count
gender_country = tweets_df.groupby(['Country', 'Gender']).size().unstack(fill_value=0)
gender_country['Total'] = gender_country.sum(axis=1)
top_countries = gender_country.sort_values('Total', ascending=False).head(10)  # Top 10 countries

# Plot the chart
fig, ax = plt.subplots(figsize=(10, 6))
top_countries.drop(columns='Total').plot(kind='bar', stacked=True, ax=ax, color=['pink','skyblue', 'lightgreen', 'lightcoral'])
plt.title("Gender Distribution by Top 10 Countries")
plt.xlabel("Country")
plt.ylabel("Tweet Count")
st.pyplot(fig)


##########


# Top 3 Hashtags
st.header("Top 3 Hashtags")

# Identify the top 3 hashtags
all_hashtags = [h for sublist in tweets_df['hashtags'] for h in sublist]
top_hashtags = Counter(all_hashtags).most_common(3)

for i, (hashtag, count) in enumerate(top_hashtags, start=1):
    st.subheader(f"#{hashtag} (Hashtag {i})")

    # Filter data for the current hashtag
    hashtag_data = tweets_df[tweets_df['hashtags'].apply(lambda x: hashtag in x)]

    # Metrics (First Row)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Tweets", len(hashtag_data))
    col2.metric("Retweets", hashtag_data['RetweetCount'].sum())
    col3.metric("Likes", hashtag_data['Likes'].sum())
    col4.metric("Countries", hashtag_data['Country'].nunique())

    # Metrics (Second Row)
    col5, col6, col7 = st.columns(3)
    col5.metric("Contributors", hashtag_data['UserID'].nunique())
    col6.metric("Reach", hashtag_data['Reach'].sum())


    # Tweet Activity by Hour
    st.write("### Tweet Activity by Hour")
    fig, ax = plt.subplots(figsize=(10, 6))
    hashtag_data['Hour'].value_counts().sort_index().plot(kind='bar', ax=ax, color='orange')
    plt.title(f"Tweet Activity by Hour for #{hashtag}")
    plt.xlabel("Hour of Day")
    plt.ylabel("Tweet Count")
    st.pyplot(fig)

    # Sentiment Distribution
    st.write("### Sentiment Distribution")
    sentiment_counts = hashtag_data['SentimentCategory'].value_counts()
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.pie(
        sentiment_counts.values,
        labels=sentiment_counts.index,
        autopct='%1.1f%%',
        startangle=140,
        colors=['#FF9999', '#66B2FF', '#99FF99']
    )
    ax.set_title(f"Sentiment Distribution for #{hashtag}")
    st.pyplot(fig)

    # World Map for Reach
    st.write("### Reach by Country")
    country_reach = hashtag_data.groupby('Country')['Reach'].sum().reset_index()
    fig = px.choropleth(
        country_reach,
        locations="Country",
        locationmode="country names",
        color="Reach",
        hover_name="Country",
        title=f"Reach by Country for #{hashtag}",
        color_continuous_scale="Viridis"
    )
    st.plotly_chart(fig)



