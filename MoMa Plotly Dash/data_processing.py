import pandas as pd
from textblob import TextBlob
from nltk.sentiment import SentimentIntensityAnalyzer
try:
    from nrclex import NRCLex
except ImportError:
    NRCLex = None

def load_data(csv_path='reviews-1.csv'):
    # Load CSV data
    df = pd.read_csv(csv_path)

    # Combine Title and Text for analysis
    df['ReviewText'] = df['Title'].fillna('') + ' ' + df['Text'].fillna('')

    # Create a datetime column
    df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']])

    # Extract City and Country from Hometown if possible
    df['City'] = df['Hometown'].str.split(',').str[0].str.strip()
    df['Country'] = df['Hometown'].str.split(',').str[-1].str.strip()
    # Handle missing values
    df['City'] = df['City'].fillna('Unknown')
    df['Country'] = df['Country'].fillna('Unknown')
    # Map US states to 'USA' in Country
    us_states = set([
        'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado',
        'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho',
        'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana',
        'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota',
        'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada',
        'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
        'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon',
        'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
        'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
        'West Virginia', 'Wisconsin', 'Wyoming'
    ])
    df['Country'] = df['Country'].apply(lambda x: 'USA' if x in us_states else x)

    # Classify Tourist Type: Local / Domestic / Foreign / Not Specified
    def classify_tourist(city, country):
        if city == 'Unknown' or country == 'Unknown' or pd.isna(city) or pd.isna(country):
            return 'Not Specified'
        # Local if from NYC area
        local_keywords = ['New York', 'NYC', 'Brooklyn', 'Manhattan', 'Queens', 'Bronx']
        if country == 'USA':
            for kw in local_keywords:
                if kw.lower() in str(city).lower():
                    return 'Local'
            return 'Domestic'
        else:
            return 'Foreign'
    df['TouristType'] = df.apply(lambda row: classify_tourist(row['City'], row['Country']), axis=1)

    # Compute sentiment scores: TextBlob and VADER
    df['TextBlob'] = df['ReviewText'].apply(lambda txt: TextBlob(txt).sentiment.polarity)
    vader = SentimentIntensityAnalyzer()
    df['VADER'] = df['ReviewText'].apply(lambda txt: vader.polarity_scores(str(txt))['compound'])
    df['Composite'] = (df['TextBlob'] + df['VADER']) / 2.0
    # Composite sentiment category
    df['Sentiment'] = df['Composite'].apply(lambda c: 'Positive' if c > 0 else ('Negative' if c < 0 else 'Neutral'))

    # Compute dominant emotion using NRCLex (if installed)
    def get_emotion(txt):
        if NRCLex is None:
            return None
        try:
            emotion = NRCLex(txt)
            top = emotion.top_emotions
            if top:
                return top[0][0]
        except:
            return None
        return None
    df['Emotion'] = df['ReviewText'].apply(get_emotion) if NRCLex else None

    return df

# Global DataFrame accessible to all pages
reviews_df = load_data()
