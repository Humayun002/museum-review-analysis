import streamlit as st
import pandas as pd
import numpy as np
import nltk
import plotly.express as px
from textblob import TextBlob
from nrclex import NRCLex
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from wordcloud import WordCloud, STOPWORDS
from sklearn.feature_extraction.text import CountVectorizer
# make sure the VADER lexicon is available
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('punkt')
nltk.download('stopwords')

# Configure page layout
st.set_page_config(page_title="MoMA Reviews Dashboard", layout="wide")

@st.cache_data
def load_and_preprocess_data():
    df = pd.read_csv('reviews-1.csv')
    # Parse date parts and combine into a datetime
    df['Year'] = df['Year']
    df['Month'] = df['Month']
    df['YearMonth'] = pd.to_datetime(df[['Year','Month']].assign(DAY=1))
    # Extract city and state/country
    df['City'] = df['Hometown'].fillna('').apply(lambda x: x.split(',')[0] if x else None)
    df['State/Country'] = df['Hometown'].fillna('').apply(
        lambda x: x.split(',')[-1].strip() if x else None
    )
    # Classify Tourist Type
    us_states = {"Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida",
                 "Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine",
                 "Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska",
                 "Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota",
                 "Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee",
                 "Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming","District of Columbia"}
    def classify_tourist(hometown):
        if pd.isna(hometown) or not isinstance(hometown, str) or hometown.strip()=="":
            return "Not Specified"
        parts = [p.strip() for p in hometown.split(',')]
        # Single token (likely state or country)
        if len(parts) == 1:
            if parts[0] in us_states:
                return "Domestic"
            else:
                return "Foreign"
        # Two-part (city, region)
        city, region = parts[0], parts[-1]
        if region in us_states:
            # In New York state -> treat as Local (NYC area)
            if region == "New York":
                return "Local"
            else:
                return "Domestic"
        return "Foreign"
    df['Tourist Type'] = df['Hometown'].apply(classify_tourist)
    # Sentiment analysis
    sid = SentimentIntensityAnalyzer()
    df['Text'] = df['Text'].fillna('')
    df['TextBlob'] = df['Text'].apply(lambda x: TextBlob(x).sentiment.polarity)
    df['VADER'] = df['Text'].apply(lambda x: sid.polarity_scores(x)['compound'])
    df['Composite'] = (df['TextBlob'] + df['VADER']) / 2
    # Classify sentiment label
    def get_sentiment_label(c):
        if c > 0.05:
            return "Positive"
        elif c < -0.05:
            return "Negative"
        else:
            return "Neutral"
    df['Sentiment'] = df['VADER'].apply(get_sentiment_label)
    # Emotion classification (dominant emotion)
    df['Emotion'] = df['Text'].apply(lambda x: NRCLex(x).top_emotions[0][0] if x else None)
    return df

data = load_and_preprocess_data()

st.sidebar.header("Filter Reviews")

years = sorted(data['Year'].unique())
selected_years = st.sidebar.multiselect("Year", options=years, default=years)

tourist_options = ["Foreign","Domestic","Local","Not Specified"]
selected_tourists = st.sidebar.multiselect("Tourist Type", options=tourist_options, default=tourist_options)

sentiment_options = ["Positive","Neutral","Negative"]
selected_sentiments = st.sidebar.multiselect("Sentiment", options=sentiment_options, default=sentiment_options)

keyword = st.sidebar.text_input("Keyword Search")

# Apply filters
filtered = data[
    data['Year'].isin(selected_years) &
    data['Tourist Type'].isin(selected_tourists) &
    data['Sentiment'].isin(selected_sentiments)
].copy()
if keyword:
    filtered = filtered[filtered['Text'].str.contains(keyword, case=False, na=False)]

st.subheader("Review Rating Distribution")
st.write("Number of reviews by rating (1 = lowest, 5 = highest).")
rating_counts = filtered['Rating'].value_counts().sort_index()
fig_rating = px.bar(
    x=rating_counts.index,
    y=rating_counts.values,
    labels={'x': 'Rating', 'y': 'Number of Reviews'},
    text=rating_counts.values
)
fig_rating.update_traces(marker_color='steelblue', textposition='outside')
fig_rating.update_layout(yaxis=dict(tick0=0, dtick=5))
st.plotly_chart(fig_rating, use_container_width=True)

st.subheader("Reviews by Tourist Type")
st.write("Count of reviews by category of visitor origin.")
tourist_counts = filtered['Tourist Type'].value_counts()
fig_tourist = px.bar(
    x=tourist_counts.index,
    y=tourist_counts.values,
    labels={'x': 'Tourist Type', 'y': 'Number of Reviews'},
    color=tourist_counts.index,
)
fig_tourist.update_layout(showlegend=False)
st.plotly_chart(fig_tourist, use_container_width=True)

with st.expander("Reviews Over Time (Yearly vs Monthly)", expanded=True):
    tab_year, tab_month = st.tabs(["Yearly Trend", "Monthly Trend"])
    # Yearly
    with tab_year:
        st.write("Annual number of reviews over time.")
        year_counts = filtered.groupby('Year').size().reset_index(name='Count')
        fig_year = px.line(
            year_counts, x='Year', y='Count', markers=True,
            labels={'Count': 'Number of Reviews'}
        )
        fig_year.update_traces(line=dict(color='teal'))
        st.plotly_chart(fig_year, use_container_width=True)
    # Monthly
    with tab_month:
        st.write("Number of reviews per month (time series).")
        month_counts = filtered.groupby('YearMonth').size().reset_index(name='Count')
        fig_month = px.line(
            month_counts, x='YearMonth', y='Count', markers=True,
            labels={'YearMonth': 'Month', 'Count': 'Number of Reviews'}
        )
        fig_month.update_traces(line=dict(color='teal'))
        st.plotly_chart(fig_month, use_container_width=True)

with st.expander("Top Reviewer Locations", expanded=False):
    st.write("Most common cities and states/countries of reviewers.")
    city_counts = filtered['City'].value_counts().head(10)
    state_counts = filtered['State/Country'].value_counts().head(10)

    fig_cities = px.bar(
        x=city_counts.values, y=city_counts.index, orientation='h',
        labels={'x': 'Number of Reviews', 'y': 'City'},
        title="Top Cities"
    )
    fig_states = px.bar(
        x=state_counts.values, y=state_counts.index, orientation='h',
        labels={'x': 'Number of Reviews', 'y': 'State/Country'},
        title="Top States/Countries"
    )
    fig_cities.update_traces(marker_color='mediumpurple')
    fig_states.update_traces(marker_color='mediumpurple')

    col1, col2 = st.columns(2)
    col1.plotly_chart(fig_cities, use_container_width=True)
    col2.plotly_chart(fig_states, use_container_width=True)

st.subheader("Monthly Average Rating Over Time")
st.write("Trend of average rating per month for the selected data.")
avg_rating = filtered.groupby(['YearMonth'])['Rating'].mean().reset_index()
fig_avg = px.line(
    avg_rating, x='YearMonth', y='Rating', markers=True,
    labels={'YearMonth': 'Month', 'Rating': 'Average Rating'}
)
fig_avg.update_traces(line=dict(color='orange'))
st.plotly_chart(fig_avg, use_container_width=True)

with st.expander("Word Clouds (Unigrams & Bigrams)", expanded=False):
    st.write("Word clouds of most frequent words (unigrams) and word pairs (bigrams) in reviews.")
    text_all = " ".join(filtered['Text'].tolist()).lower()
    # Unigram word cloud
    wc1 = WordCloud(width=400, height=300, background_color='white',
                    stopwords=set(STOPWORDS)).generate(text_all)
    st.image(wc1.to_array(), caption="Unigram Word Cloud")
    # Bigram word cloud (using frequencies)
    vectorizer = CountVectorizer(ngram_range=(2,2), stop_words='english')
    X = vectorizer.fit_transform(filtered['Text'])
    bigram_freq = dict(zip(vectorizer.get_feature_names_out(), X.sum(axis=0).A1))
    wc2 = WordCloud(width=400, height=300, background_color='white',
                    stopwords=set(STOPWORDS)).generate_from_frequencies(bigram_freq)
    st.image(wc2.to_array(), caption="Bigram Word Cloud")

with st.expander("Sentiment Distribution", expanded=False):
    st.write("Distribution of review sentiment (via VADER classification) for selected reviews.")
    overall_tab, byyear_tab = st.tabs(["Overall Sentiment", "Sentiment by Year"])
    # Overall sentiment pie/bar
    with overall_tab:
        sent_counts = filtered['Sentiment'].value_counts()
        fig_sent = px.bar(
            x=sent_counts.index, y=sent_counts.values,
            labels={'x': 'Sentiment', 'y': 'Number of Reviews'},
            color=sent_counts.index
        )
        fig_sent.update_layout(showlegend=False)
        st.plotly_chart(fig_sent, use_container_width=True)
    # Sentiment by year (grouped bar)
    with byyear_tab:
        year_sent = filtered.groupby(['Year','Sentiment']).size().reset_index(name='Count')
        fig_yearsent = px.bar(
            year_sent, x='Year', y='Count', color='Sentiment', barmode='group',
            labels={'Count': 'Number of Reviews'}
        )
        st.plotly_chart(fig_yearsent, use_container_width=True)

st.subheader("Sentiment Score Comparison by Year")
st.write("Average sentiment scores by year (TextBlob vs VADER vs composite).")
score_avg = filtered.groupby('Year').agg({
    'TextBlob': 'mean',
    'VADER': 'mean',
    'Composite': 'mean'
}).reset_index()
score_melted = score_avg.melt(id_vars=['Year'], 
                              value_vars=['TextBlob','VADER','Composite'],
                              var_name='Method', value_name='Score')
fig_scores = px.line(
    score_melted, x='Year', y='Score', color='Method', markers=True,
    labels={'Score': 'Mean Sentiment Score'}
)
st.plotly_chart(fig_scores, use_container_width=True)

st.subheader("Emotion Classification (Dominant Emotion)")
st.write("Predicted dominant emotion in each review (via NRC Lexicon).")
emotion_counts = filtered['Emotion'].value_counts()
fig_emotion = px.bar(
    x=emotion_counts.index, y=emotion_counts.values,
    labels={'x': 'Emotion', 'y': 'Number of Reviews'},
    color=emotion_counts.index
)
fig_emotion.update_layout(showlegend=False)
st.plotly_chart(fig_emotion, use_container_width=True)

with st.expander("Common Words in Negative Reviews", expanded=False):
    st.write("Top words in reviews classified as Negative (sentiment).")
    neg_reviews = filtered[filtered['Sentiment'] == 'Negative']
    neg_text = " ".join(neg_reviews['Text'].tolist())
    vec = CountVectorizer(stop_words='english')
    X_neg = vec.fit_transform(neg_reviews['Text'])
    word_freq = dict(zip(vec.get_feature_names_out(), X_neg.sum(axis=0).A1))
    top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
    df_top = pd.DataFrame(top_words, columns=['Word','Count'])
    fig_negwords = px.bar(
        df_top, x='Count', y='Word', orientation='h',
        labels={'Count': 'Frequency', 'Word': 'Word'}
    )
    st.plotly_chart(fig_negwords, use_container_width=True)

