import kivy
kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.camera import Camera
from kivy.clock import Clock
from kivy.uix.label import Label

import numpy as np
import cv2

from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.utils import img_to_array
from tensorflow.keras.models import load_model
import MFG598_Movie_Recommend_Emotion_Based as app2



class FullScreenImageScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.image = Image(source='C.png', allow_stretch=True, keep_ratio=False)
        self.add_widget(self.image)
        
        self.next_page_button = Button(text='Next Page', size_hint=(1.0, 0.05), size=(100, 50), pos=(0, 0))
        self.next_page_button.bind(on_press=self.switch_to_camera_screen)
        self.add_widget(self.next_page_button)

    def switch_to_camera_screen(self, *args):
        app = App.get_running_app()
        app.sm.current = 'camera_screen'
        

class CameraScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera = Camera(resolution=(640, 480), play=True, allow_stretch=True, keep_ratio=False)
        self.add_widget(self.camera)

        self.countdown_label = Label(text="5", font_size=50, pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.add_widget(self.countdown_label)
        
        self.photo_countdown = 5 # countdown time in seconds
        self.photo_interval = None
        
    def on_enter(self):
        # start the photo countdown when the screen is entered
        self.photo_interval = Clock.schedule_interval(self.take_photo, 1.0)
        
    def on_leave(self):
        # cancel the photo countdown when the screen is left
        if self.photo_interval:
            self.photo_interval.cancel()
        
    def take_photo(self, dt):
        self.photo_countdown -= 1
        self.countdown_label.text = str(self.photo_countdown)
        if self.photo_countdown <= 0:
            # take the photo
            self.camera.export_to_png("photo.png")
            # switch to the emotion screen
            app = App.get_running_app()
            app.sm.current = 'emotion_screen'
        else:
            # update the countdown label
            self.countdown_label.text = str(self.photo_countdown)

class EmotionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = Label(text='', font_size=50, pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.add_widget(self.label)

    def on_enter(self):
        # load the facial expression recognition model
        model = load_model('ferNet.h5')
        
        # load the image and preprocess it
        image = load_img('photo.png', grayscale=True, target_size=(48, 48))
        x = img_to_array(image)
        x = np.expand_dims(x, axis=0)
        x /= 255
        
        # predict the emotion from the image
        emotion_labels = {0: 'Angry', 1: 'Disgust', 2: 'Fear', 3: 'Happy', 4: 'Sad', 5: 'Surprise', 6: 'Neutral'}
        prediction = model.predict(x)
        max_index = np.argmax(prediction[0])
        self.emotions = emotion_labels[max_index]
        
        # display the predicted emotion on the screen
        self.label.text = self.emotions
        self.next_button = Button(text="Next", size_hint=(1.0, 0.05), size=(100, 50), pos=(0, 25))
        self.next_button.bind(on_press=self.exit_app)
        # add a button to retake the photo
        self.retake_button = Button(text='Retake Photo', size_hint=(1.0, 0.05), size=(100, 50), pos=(0, 0))
        self.retake_button.bind(on_press=self.switch_to_camera_screen)
        self.add_widget(self.retake_button)
        
        # add a button to go back to the home screen
        self.home_button = Button(text='Home', size_hint=(1.0, 0.05), size=(100, 50), pos=(0, 50))
        self.home_button.bind(on_press=self.switch_to_home_screen)
        self.add_widget(self.home_button)
        self.add_widget(self.next_button)

    def switch_to_camera_screen(self, *args):
        app = App.get_running_app()
        app.sm.current = 'camera_screen'

    def switch_to_home_screen(self, *args):
        app = App.get_running_app()
        app.sm.current = 'home_screen'
    
    def exit_app(self, *args):
        f = open("emotion_out.txt", "w")
        f.write(self.emotions)
        f.close()
        
        App.get_running_app().stop()
        
        

 
class WindowManager(ScreenManager):
    pass


class EmotionDetectorApp(App):
    def build(self):
        self.sm = WindowManager()
        
        self.home_screen = FullScreenImageScreen(name='home_screen')
        self.sm.add_widget(self.home_screen)

        self.camera_screen = CameraScreen(name='camera_screen')
        self.sm.add_widget(self.camera_screen)

        self.emotion_screen = EmotionScreen(name='emotion_screen')
        self.sm.add_widget(self.emotion_screen)
        
        return self.sm



if __name__ == '__main__':
    EmotionDetectorApp().run()
