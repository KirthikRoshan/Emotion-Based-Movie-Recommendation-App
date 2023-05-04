# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 08:12:42 2023

@author: KirthikRoshan
"""


from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.properties import ListProperty
import pandas as pd

class MovieApp(App):
    movie_titles = ListProperty([])
    start_index = 0
    num_movies = 5
    
    def build(self):
        # Load data from combined1.csv file
        with open('emotion_out.txt') as f:
            lines = f.readlines()
        print(lines)
        data = pd.read_csv(str(lines[0])+'.csv')

        # Create a float layout for the app
        layout = FloatLayout()

        # Add an image to the float layout
        image = Image(source='c.jpg', allow_stretch=True, keep_ratio=False)
        layout.add_widget(image)

        # Loop through the next set of rows in the data and create buttons for each movie
        for i in range(self.start_index, self.start_index+self.num_movies):
            # Get the movie title, rating, and genre
            title = data.iloc[i]['title']
            rating = data.iloc[i]['weightedAverage']
            genres = data.iloc[i]['genres']

            # Create a button for the movie title
            button = Button(text=f'{title} ({genres}) - Rating: {rating}', size_hint=(0.7, 0.1), pos_hint={'x': 0.15, 'y': 0.4})
            button.bind(on_press=self.on_button_press)
            self.movie_titles.append(title)
            layout.add_widget(button)

        # Add a "Next" button to display the next set of movies
        next_button = Button(text='Next', size_hint=(0.1, 0.1), pos_hint={'x': 0.45, 'y': 0.3})
        next_button.bind(on_press=self.on_next_button_press)
        layout.add_widget(next_button)

        return layout

    def on_button_press(self, button):
        title = button.text.split('(')[0].strip()
        print(f'Selected movie: {title}')
        with open('selected_movie.txt', 'w') as f:
            f.write(title)   
        
    def on_next_button_press(self, button):
        # Update the start_index to display the next set of movies
        self.start_index += self.num_movies

        # Reload the data and rebuild the UI with the next set of movies
        with open('emotion_out.txt') as f:
            lines = f.readlines()
        print(lines)
        data = pd.read_csv(str(lines[0])+'.csv')
        layout = self.build()
        button.parent.add_widget(layout)

if __name__ == '__main__':
    MovieApp().run()