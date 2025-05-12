from dash import dcc, html
from dash.dependencies import Input, Output
from data_processing import reviews_df

layout = html.Div([
    html.H2("Overview"),
    html.Div(id='stats-container'),
    html.Div([
        dcc.Graph(id='rating-dist-graph', style={'width': '48%', 'display': 'inline-block'}),
        dcc.Graph(id='tourist-dist-graph', style={'width': '48%', 'display': 'inline-block'})
    ]),
    dcc.Tabs([
        dcc.Tab(label='Yearly Reviews', children=[
            dcc.Graph(id='yearly-reviews-graph')
        ]),
        dcc.Tab(label='Monthly Reviews', children=[
            dcc.Graph(id='monthly-reviews-graph')
        ])
    ]),
    html.Div([
        dcc.Graph(id='top-cities-graph', style={'width': '48%', 'display': 'inline-block'}),
        dcc.Graph(id='top-countries-graph', style={'width': '48%', 'display': 'inline-block'})
    ]),
    dcc.Graph(id='monthly-avg-rating-graph')
])

def register_callbacks(app):
    # Data filtering helper (applies all global filters)
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

    # Update descriptive stats (total, mean, median)
    @app.callback(
        Output('stats-container', 'children'),
        [Input('year-filter', 'value'),
         Input('tourist-filter', 'value'),
         Input('sentiment-filter', 'value'),
         Input('rating-filter', 'value'),
         Input('keyword-filter', 'value')]
    )
    def update_stats(years, tourist_types, sentiments, ratings, keyword):
        dff = filter_df(years, tourist_types, sentiments, ratings, keyword)
        total_reviews = dff.shape[0]
        mean_rating = dff['Rating'].mean() if total_reviews > 0 else 0
        median_rating = dff['Rating'].median() if total_reviews > 0 else 0
        return [
            html.P(f"Total Reviews: {total_reviews}"),
            html.P(f"Mean Rating: {mean_rating:.2f}"),
            html.P(f"Median Rating: {median_rating:.2f}")
        ]

    # Ratings distribution bar chart
    @app.callback(
        Output('rating-dist-graph', 'figure'),
        [Input('year-filter', 'value'),
         Input('tourist-filter', 'value'),
         Input('sentiment-filter', 'value'),
         Input('rating-filter', 'value'),
         Input('keyword-filter', 'value')]
    )
    def update_rating_dist(years, tourist_types, sentiments, ratings, keyword):
        dff = filter_df(years, tourist_types, sentiments, ratings, keyword)
        counts = dff['Rating'].value_counts().sort_index()
        fig = {
            'data': [{'x': counts.index.tolist(), 'y': counts.values.tolist(), 'type': 'bar'}],
            'layout': {'title': 'Rating Distribution', 'xaxis': {'title': 'Rating'}, 'yaxis': {'title': 'Count'}}
        }
        return fig

    # Tourist type distribution bar chart
    @app.callback(
        Output('tourist-dist-graph', 'figure'),
        [Input('year-filter', 'value'),
         Input('tourist-filter', 'value'),
         Input('sentiment-filter', 'value'),
         Input('rating-filter', 'value'),
         Input('keyword-filter', 'value')]
    )
    def update_tourist_dist(years, tourist_types, sentiments, ratings, keyword):
        dff = filter_df(years, tourist_types, sentiments, ratings, keyword)
        counts = dff['TouristType'].value_counts()
        fig = {
            'data': [{'x': counts.index.tolist(), 'y': counts.values.tolist(), 'type': 'bar'}],
            'layout': {'title': 'Tourist Type Distribution', 'xaxis': {'title': 'Type'}, 'yaxis': {'title': 'Count'}}
        }
        return fig

    # Reviews per year line chart
    @app.callback(
        Output('yearly-reviews-graph', 'figure'),
        [Input('year-filter', 'value'),
         Input('tourist-filter', 'value'),
         Input('sentiment-filter', 'value'),
         Input('rating-filter', 'value'),
         Input('keyword-filter', 'value')]
    )
    def update_yearly_reviews(years, tourist_types, sentiments, ratings, keyword):
        dff = filter_df(years, tourist_types, sentiments, ratings, keyword)
        yearly_counts = dff.groupby('Year').size()
        fig = {
            'data': [{'x': yearly_counts.index.tolist(), 'y': yearly_counts.values.tolist(), 'type': 'line'}],
            'layout': {'title': 'Reviews per Year', 'xaxis': {'title': 'Year'}, 'yaxis': {'title': 'Count'}}
        }
        return fig

    # Reviews by month line chart (all years aggregated)
    @app.callback(
        Output('monthly-reviews-graph', 'figure'),
        [Input('year-filter', 'value'),
         Input('tourist-filter', 'value'),
         Input('sentiment-filter', 'value'),
         Input('rating-filter', 'value'),
         Input('keyword-filter', 'value')]
    )
    def update_monthly_reviews(years, tourist_types, sentiments, ratings, keyword):
        dff = filter_df(years, tourist_types, sentiments, ratings, keyword)
        if dff.empty:
            months, counts = [], []
        else:
            monthly_counts = dff.groupby('Month').size().sort_index()
            months = monthly_counts.index.tolist()
            counts = monthly_counts.values.tolist()
        fig = {
            'data': [{'x': months, 'y': counts, 'type': 'line'}],
            'layout': {'title': 'Reviews by Month (All Years)', 'xaxis': {'title': 'Month'}, 'yaxis': {'title': 'Count'}}
        }
        return fig

    # Top cities bar chart
    @app.callback(
        Output('top-cities-graph', 'figure'),
        [Input('year-filter', 'value'),
         Input('tourist-filter', 'value'),
         Input('sentiment-filter', 'value'),
         Input('rating-filter', 'value'),
         Input('keyword-filter', 'value')]
    )
    def update_top_cities(years, tourist_types, sentiments, ratings, keyword):
        dff = filter_df(years, tourist_types, sentiments, ratings, keyword)
        city_counts = dff['City'].value_counts().nlargest(10)
        fig = {
            'data': [{'x': city_counts.index.tolist(), 'y': city_counts.values.tolist(), 'type': 'bar'}],
            'layout': {'title': 'Top Cities', 'xaxis': {'title': 'City'}, 'yaxis': {'title': 'Count'}}
        }
        return fig

    # Top countries bar chart
    @app.callback(
        Output('top-countries-graph', 'figure'),
        [Input('year-filter', 'value'),
         Input('tourist-filter', 'value'),
         Input('sentiment-filter', 'value'),
         Input('rating-filter', 'value'),
         Input('keyword-filter', 'value')]
    )
    def update_top_countries(years, tourist_types, sentiments, ratings, keyword):
        dff = filter_df(years, tourist_types, sentiments, ratings, keyword)
        country_counts = dff['Country'].value_counts().nlargest(10)
        fig = {
            'data': [{'x': country_counts.index.tolist(), 'y': country_counts.values.tolist(), 'type': 'bar'}],
            'layout': {'title': 'Top Countries', 'xaxis': {'title': 'Country'}, 'yaxis': {'title': 'Count'}}
        }
        return fig

    # Average rating by month line chart
    @app.callback(
        Output('monthly-avg-rating-graph', 'figure'),
        [Input('year-filter', 'value'),
         Input('tourist-filter', 'value'),
         Input('sentiment-filter', 'value'),
         Input('rating-filter', 'value'),
         Input('keyword-filter', 'value')]
    )
    def update_monthly_avg_rating(years, tourist_types, sentiments, ratings, keyword):
        dff = filter_df(years, tourist_types, sentiments, ratings, keyword)
        if dff.empty:
            months, avg_vals = [], []
        else:
            avg_ratings = dff.groupby('Month')['Rating'].mean().reindex(range(1,13)).fillna(0)
            months = avg_ratings.index.tolist()
            avg_vals = avg_ratings.values.tolist()
        fig = {
            'data': [{'x': months, 'y': avg_vals, 'type': 'line'}],
            'layout': {'title': 'Average Rating by Month', 'xaxis': {'title': 'Month'}, 'yaxis': {'title': 'Avg Rating'}}
        }
        return fig
