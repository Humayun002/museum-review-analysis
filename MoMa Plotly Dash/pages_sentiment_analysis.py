from dash import dcc, html
from dash.dependencies import Input, Output
from data_processing import reviews_df

layout = html.Div([
    html.H2("Sentiment Analysis"),
    html.Div([
        dcc.Graph(id='sentiment-dist-overall', style={'width': '48%', 'display': 'inline-block'}),
        dcc.Graph(id='sentiment-dist-yearly', style={'width': '48%', 'display': 'inline-block'})
    ]),
    dcc.Graph(id='sentiment-line-graph')
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
        Output('sentiment-dist-overall', 'figure'),
        [Input('year-filter', 'value'),
         Input('tourist-filter', 'value'),
         Input('sentiment-filter', 'value'),
         Input('rating-filter', 'value'),
         Input('keyword-filter', 'value')]
    )
    def update_sentiment_dist_overall(years, tourist_types, sentiments, ratings, keyword):
        dff = filter_df(years, tourist_types, sentiments, ratings, keyword)
        counts = dff['Sentiment'].value_counts()
        fig = {
            'data': [{'x': counts.index.tolist(), 'y': counts.values.tolist(), 'type': 'bar'}],
            'layout': {'title': 'Sentiment Distribution (Overall)', 'xaxis': {'title': 'Sentiment'}, 'yaxis': {'title': 'Count'}}
        }
        return fig

    @app.callback(
        Output('sentiment-dist-yearly', 'figure'),
        [Input('year-filter', 'value'),
         Input('tourist-filter', 'value'),
         Input('sentiment-filter', 'value'),
         Input('rating-filter', 'value'),
         Input('keyword-filter', 'value')]
    )
    def update_sentiment_dist_yearly(years, tourist_types, sentiments, ratings, keyword):
        dff = filter_df(years, tourist_types, sentiments, ratings, keyword)
        fig_data = []
        if not dff.empty:
            years_sorted = sorted(dff['Year'].unique())
            sentiments_order = ['Positive', 'Neutral', 'Negative']
            for s in sentiments_order:
                counts = []
                for y in years_sorted:
                    count = dff[(dff['Year'] == y) & (dff['Sentiment'] == s)].shape[0]
                    counts.append(count)
                fig_data.append({'x': years_sorted, 'y': counts, 'name': s, 'type': 'bar'})
        fig = {
            'data': fig_data,
            'layout': {'barmode': 'stack', 'title': 'Sentiment by Year', 'xaxis': {'title': 'Year'}, 'yaxis': {'title': 'Count'}}
        }
        return fig

    @app.callback(
        Output('sentiment-line-graph', 'figure'),
        [Input('year-filter', 'value'),
         Input('tourist-filter', 'value'),
         Input('sentiment-filter', 'value'),
         Input('rating-filter', 'value'),
         Input('keyword-filter', 'value')]
    )
    def update_sentiment_line(years, tourist_types, sentiments, ratings, keyword):
        dff = filter_df(years, tourist_types, sentiments, ratings, keyword)
        fig_data = []
        if not dff.empty:
            yearly = dff.groupby('Year').agg({
                'TextBlob': 'mean', 'VADER': 'mean', 'Composite': 'mean'
            }).reset_index()
            fig_data.append({'x': yearly['Year'].tolist(), 'y': yearly['TextBlob'].tolist(), 'name': 'TextBlob', 'mode': 'lines+markers'})
            fig_data.append({'x': yearly['Year'].tolist(), 'y': yearly['VADER'].tolist(), 'name': 'VADER', 'mode': 'lines+markers'})
            fig_data.append({'x': yearly['Year'].tolist(), 'y': yearly['Composite'].tolist(), 'name': 'Composite', 'mode': 'lines+markers'})
        fig = {
            'data': fig_data,
            'layout': {'title': 'Average Sentiment Scores by Year', 'xaxis': {'title': 'Year'}, 'yaxis': {'title': 'Average Score'}}
        }
        return fig
