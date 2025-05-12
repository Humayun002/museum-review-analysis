from dash import dcc, html
from dash.dependencies import Input, Output
from data_processing import reviews_df
from sklearn.feature_extraction.text import CountVectorizer

layout = html.Div([
    html.H2("Negative Review Analysis"),
    html.Label("Filter by Emotion:"),
    dcc.Dropdown(
        id='negative-emotion-filter',
        options=[
            {'label': emo.capitalize(), 'value': emo} for emo in 
            ['fear','anger','anticipation','trust','surprise','positive','negative','sadness','joy','disgust']
        ],
        placeholder='Select emotion',
        multi=False
    ),
    dcc.Graph(id='negative-keywords-graph')
])

def register_callbacks(app):
    # Data filtering helper (always filter for negative sentiment)
    def filter_df(emotion, years, tourist_types, ratings, keyword):
        df = reviews_df.copy()
        df = df[df['Sentiment'] == 'Negative']
        if years:
            df = df[df['Year'].isin(years)]
        if tourist_types:
            df = df[df['TouristType'].isin(tourist_types)]
        if ratings:
            df = df[df['Rating'].isin(ratings)]
        if keyword:
            df = df[df['ReviewText'].str.contains(keyword, case=False, na=False)]
        if emotion:
            df = df[df['Emotion'] == emotion]
        return df

    @app.callback(
        Output('negative-keywords-graph', 'figure'),
        [Input('negative-emotion-filter', 'value'),
         Input('year-filter', 'value'),
         Input('tourist-filter', 'value'),
         Input('rating-filter', 'value'),
         Input('keyword-filter', 'value')]
    )
    def update_negative_keywords(emotion, years, tourist_types, ratings, keyword):
        dff = filter_df(emotion, years, tourist_types, ratings, keyword)
        texts = dff['ReviewText'].dropna().tolist()
        if not texts:
            return {'data': [], 'layout': {'title': 'Top Keywords in Negative Reviews'}}
        vectorizer = CountVectorizer(stop_words='english')
        X = vectorizer.fit_transform(texts)
        freqs = dict(zip(vectorizer.get_feature_names_out(), X.toarray().sum(axis=0)))
        top_words = sorted(freqs.items(), key=lambda x: x[1], reverse=True)[:10]
        words = [w for w, _ in top_words]
        counts = [cnt for _, cnt in top_words]
        fig = {
            'data': [{'x': words, 'y': counts, 'type': 'bar'}],
            'layout': {'title': 'Top Keywords in Negative Reviews', 'xaxis': {'title': 'Word'}, 'yaxis': {'title': 'Count'}}
        }
        return fig
