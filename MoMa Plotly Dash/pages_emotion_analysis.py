    from dash import dcc, html
from dash.dependencies import Input, Output
from data_processing import reviews_df

layout = html.Div([
    html.H2("Emotion Analysis"),
    dcc.Graph(id='emotion-dist-graph')
])

def register_callbacks(app):
    # Data filtering helper
    def filter_df(years, tourist_types, sentiments, ratings, keyword):
        df = reviews_df.copy()
        if years:
            df = df[df['Year'].isin(years)]
        if tourist_types:
            df = df[df['TouristType'].isin(tourist_types)]
        if sentiments:
            df = df[df['Sentiment'].isin(sentiments)]
        if ratings:
            df = df[df['Rating'].isin(ratings)]
        if keyword:
            df = df[df['ReviewText'].str.contains(keyword, case=False, na=False)]
        return df

    @app.callback(
        Output('emotion-dist-graph', 'figure'),
        [Input('year-filter', 'value'),
         Input('tourist-filter', 'value'),
         Input('sentiment-filter', 'value'),
         Input('rating-filter', 'value'),
         Input('keyword-filter', 'value')]
    )
    def update_emotion_dist(years, tourist_types, sentiments, ratings, keyword):
        dff = filter_df(years, tourist_types, sentiments, ratings, keyword)
        if 'Emotion' not in dff or dff['Emotion'] is None:
            return {'data': [], 'layout': {'title': 'Dominant Emotions'}}
        counts = dff['Emotion'].value_counts()
        fig = {
            'data': [{'x': counts.index.tolist(), 'y': counts.values.tolist(), 'type': 'bar'}],
            'layout': {'title': 'Dominant Emotions', 'xaxis': {'title': 'Emotion'}, 'yaxis': {'title': 'Count'}}
        }
        return fig
