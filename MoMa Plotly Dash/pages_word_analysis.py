from dash import dcc, html
from dash.dependencies import Input, Output
from data_processing import reviews_df
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer
import io
import base64

layout = html.Div([
    html.H2("Word Analysis"),
    html.P("Top Unigrams"),
    html.Img(id='wordcloud-unigram', style={'maxWidth': '100%', 'height': 'auto'}),
    html.P("Top Bigrams"),
    html.Img(id='wordcloud-bigram', style={'maxWidth': '100%', 'height': 'auto'})
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
        [Output('wordcloud-unigram', 'src'),
         Output('wordcloud-bigram', 'src')],
        [Input('year-filter', 'value'),
         Input('tourist-filter', 'value'),
         Input('sentiment-filter', 'value'),
         Input('rating-filter', 'value'),
         Input('keyword-filter', 'value')]
    )
    def update_wordclouds(years, tourist_types, sentiments, ratings, keyword):
        dff = filter_df(years, tourist_types, sentiments, ratings, keyword)
        texts = dff['ReviewText'].dropna().tolist()
        if not texts:
            return "", ""
        corpus = " ".join(texts)

        # Unigram frequencies
        vec1 = CountVectorizer(stop_words='english', ngram_range=(1,1))
        X1 = vec1.fit_transform(texts)
        freq1 = dict(zip(vec1.get_feature_names_out(), X1.toarray().sum(axis=0)))
        wc1 = WordCloud(width=800, height=400, background_color='white')
        wc1.generate_from_frequencies(freq1)
        img1 = wc1.to_image()

        # Bigram frequencies
        vec2 = CountVectorizer(stop_words='english', ngram_range=(2,2))
        X2 = vec2.fit_transform(texts)
        freq2 = dict(zip(vec2.get_feature_names_out(), X2.toarray().sum(axis=0)))
        wc2 = WordCloud(width=800, height=400, background_color='white')
        wc2.generate_from_frequencies(freq2)
        img2 = wc2.to_image()

        # Convert images to base64 strings for embedding
        buffer1 = io.BytesIO()
        img1.save(buffer1, format="PNG")
        img_str1 = base64.b64encode(buffer1.getvalue()).decode()
        src1 = "data:image/png;base64," + img_str1

        buffer2 = io.BytesIO()
        img2.save(buffer2, format="PNG")
        img_str2 = base64.b64encode(buffer2.getvalue()).decode()
        src2 = "data:image/png;base64," + img_str2

        return src1, src2
