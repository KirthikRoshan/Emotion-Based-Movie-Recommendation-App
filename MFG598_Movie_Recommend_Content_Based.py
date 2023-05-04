import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

# Load data and perform necessary preprocessing
df1 = pd.read_csv('tmdb_5000_credits.csv')
df2 = pd.read_csv('tmdb_5000_movies.csv')
df1.columns = ['id','title','cast','crew']
df2 = df2.merge(df1, on='id')

C= df2['vote_average'].mean()
m= df2['vote_count'].quantile(0.9)
q_movies = df2.copy().loc[df2['vote_count'] >= m]

def weighted_rating(x, m=m, C=C):
    v = x['vote_count']
    R = x['vote_average']
    # Calculation based on the IMDB formula
    return (v/(v+m) * R) + (m/(m+v) * C)

# Define a new feature 'score' and calculate its value with `weighted_rating()`
q_movies['score'] = q_movies.apply(weighted_rating, axis=1)

#Sort movies based on score calculated above
q_movies = q_movies.sort_values('score', ascending=False)

#Print the top 15 movies
q_movies[['original_title', 'vote_count', 'vote_average', 'score']].head(10)

tfidf = TfidfVectorizer(stop_words='english')
df2['overview'] = df2['overview'].fillna('')
tfidf_matrix = tfidf.fit_transform(df2['overview'])
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
indices = pd.Series(df2.index, index=df2['original_title']).drop_duplicates()

# Define the layout of the app using Kivy language
Builder.load_string('''
<RootWidget>:
    orientation: 'vertical'
    original_title_input: original_title_input
    recommendation_output: recommendation_output
    
    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        height: '40sp'
        Label:
            text: 'Enter a movie title: '
        TextInput:
            id: original_title_input
            multiline: False
            on_text_validate: root.get_recommendations(reset_idx=True)
    
    ScrollView:
        Label:
            id: recommendation_output
            text_size: self.width, None
            size_hint_y: None
            height: self.texture_size[1]
            text: ''
''')

# Define the root widget
class RootWidget(BoxLayout):
    
    original_title_input = ObjectProperty()
    recommendation_output = ObjectProperty()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_idx = 0
    
    def get_recommendations(self, reset_idx=False):
        if reset_idx:
            self.current_idx = 0
        
        # Get the user input movie title
        original_title = self.original_title_input.text.strip()
        
        # Check if the movie exists in the dataset
        if original_title not in indices:
            self.recommendation_output.text = "Enter a different movie"
            return
        
        # Get the index of the movie that matches the title
        idx = indices[original_title]
        
        # Get the pairwise similarity scores of all movies with that movie
        sim_scores = list(enumerate(cosine_sim[idx]))
        
        # Sort the movies based on the similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)      

        # Get the indices of the 10 most similar movies
        start_idx = self.current_idx
        end_idx = start_idx + 10
        movie_indices = [i[0] for i in sim_scores[start_idx:end_idx]]
        
        # Get the titles of the most similar movies
        recommendation_titles = df2['original_title'].iloc[movie_indices].values
        
        # Format the recommendations as a string and display them in the app
        recommendation_text = '\n'.join(recommendation_titles)
        self.recommendation_output.text = recommendation_text
        
        # Increment the current index
        self.current_idx += 10

# Define the Kivy app
class MovieRecommendationApp(App):
    def build(self):
        return RootWidget()

# Run the app
if __name__ == '__main__':
    MovieRecommendationApp().run()