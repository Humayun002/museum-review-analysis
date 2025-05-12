import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from data_processing import reviews_df

import pages.overview as overview_page
import pages.word_analysis as word_page
import pages.sentiment_analysis as sentiment_page
import pages.emotion_analysis as emotion_page
import pages.negative_analysis as negative_page

# Initialize the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

# Extract unique values for filters
years = sorted(reviews_df['Year'].unique())
tourist_types = ['Foreign', 'Domestic', 'Local', 'Not Specified']
sentiments = ['Positive', 'Neutral', 'Negative']
ratings = sorted(reviews_df['Rating'].unique())

# App layout with sidebar filters and page content
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    # Navigation links at top
    html.Div([
        dcc.Link('Overview', href='/', style={'marginRight': '15px'}),
        dcc.Link('Word Analysis', href='/word-analysis', style={'marginRight': '15px'}),
        dcc.Link('Sentiment', href='/sentiment', style={'marginRight': '15px'}),
        dcc.Link('Emotion', href='/emotion', style={'marginRight': '15px'}),
        dcc.Link('Negative Reviews', href='/negative', style={'marginRight': '15px'})
    ], style={'padding': '10px', 'backgroundColor': '#f0f0f0'}),
    html.Div([
        # Sidebar for global filters
        html.Div([
            html.H4("Filters"),
            html.Label("Year:"),
            dcc.Dropdown(
                id='year-filter',
                options=[{'label': str(y), 'value': y} for y in years],
                value=years, multi=True
            ),
            html.Br(),
            html.Label("Tourist Type:"),
            dcc.Dropdown(
                id='tourist-filter',
                options=[{'label': t, 'value': t} for t in tourist_types],
                value=tourist_types, multi=True
            ),
            html.Br(),
            html.Label("Sentiment:"),
            dcc.Dropdown(
                id='sentiment-filter',
                options=[{'label': s, 'value': s} for s in sentiments],
                value=sentiments, multi=True
            ),
            html.Br(),
            html.Label("Rating:"),
            dcc.Dropdown(
                id='rating-filter',
                options=[{'label': str(r), 'value': r} for r in ratings],
                value=ratings, multi=True
            ),
            html.Br(),
            html.Label("Keyword:"),
            dcc.Input(
                id='keyword-filter',
                type='text',
                placeholder='Search reviews...',
                style={'width': '100%'}
            ),
        ], style={'width': '20%', 'display': 'inline-block', 'verticalAlign': 'top', 
                  'padding': '10px', 'backgroundColor': '#f9f9f9'}),
        # Main page content area
        html.Div(id='page-content', style={'width': '75%', 'display': 'inline-block', 'padding': '10px'})
    ], style={'display': 'flex'})
])

# Register callbacks for each page
overview_page.register_callbacks(app)
word_page.register_callbacks(app)
sentiment_page.register_callbacks(app)
emotion_page.register_callbacks(app)
negative_page.register_callbacks(app)

# Page routing callback
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/word-analysis':
        return word_page.layout
    elif pathname == '/sentiment':
        return sentiment_page.layout
    elif pathname == '/emotion':
        return emotion_page.layout
    elif pathname == '/negative':
        return negative_page.layout
    else:
        # Default: Overview page
        return overview_page.layout

if __name__ == '__main__':
    app.run_server(debug=True)
