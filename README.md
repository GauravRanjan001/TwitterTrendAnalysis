# Twitter Trend Analysis


## 1. Project Overview: 
This project focuses on analysing Twitter data to identify trending topics, hashtags, and user 
engagement patterns. The analysis focuses on understanding key engagement metrics, extracting top 
hashtags, performing sentiment analysis, visualizing temporal and geographical tweet distributions, 
and building a comprehensive dashboard to display the findings. 


## 2. Dataset Description 
The dataset used (tweetsdata.csv) consists of offline-collected tweets and includes the following key 
fields: \
• UserID, Gender, Country \
• Text (containing hashtags), Sentiment, Likes, RetweetCount, Reach \
• Timestamp, from which Hour is derived \

About Dataset: 
• File size: ~28 MB 
• Tweet Count: 100,000  
• Unique Users: 33,213 


## 3. Tools & Technologies 
• Language: Python 
• Libraries:  
  o Visualization: Matplotlib, Plotly, WordCloud 
  o Interface: Streamlit (for building interactive dashboard) 
  o Other: Pandas, collections, re, locale, etc


## 4. Methodology 
4.1 Data Preprocessing 
• Cleaned column names to remove whitespace and handled missing tweet texts by filling 
them with empty strings. 
• Extracted hashtags from tweet texts using regular expressions. 
• Categorized sentiments as Positive, Negative, or Neutral based on sentiment score. 
4.2 Metrics Computed 
• Total Tweets: Count of all tweets in the dataset. 
• Unique Contributors: Number of unique users who tweeted. 
• Total Likes, Retweets, and Reach: Aggregated metrics for engagement. 
• Total and Unique Hashtags: Count of all hashtags and unique hashtags. 
• Number of Countries represented: Count of distinct countries from which tweets originated. 
4.3 Hashtag Analysis 
• Generated a bar chart of the top 15 most frequent hashtags. 
• Created a word cloud for visual representation of trending hashtags. 
4.4 Temporal Analysis 
• Plotted tweet distribution across hours of the day to observe peak activity times. 
4.5 Sentiment Analysis 
• Analysed sentiment distribution using a histogram with a KDE curve, for numerical sentiment 
scores. 
• Categorized tweets into three sentiment classes: Positive, negative and Neutral and  
• Visualized sentiment distribution using pie chart.
