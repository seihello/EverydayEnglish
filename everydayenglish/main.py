from word import Word
from math import sqrt
from random import randint
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Point, GraphicException
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
import csv

__version__ = '1.0'

import kivy
kivy.require('1.0.6')

class EverydayEnglish(Widget):

    JAPANESE_FONT_NAME = 'ヒラギノ丸ゴ ProN W4.ttc'
    SWIPE_WIDTH = 50

    def prepare(self):

        self.orientation = 'vertical'

        with open('english.csv') as f:
            reader = csv.reader(f)
            self.word_matrix = [row for row in reader]

        self.title_label = Label(font_size=70,
                            color=(1, 0, 0, 1),
                            halign='left',
                            valign='top',
                            font_name=self.JAPANESE_FONT_NAME
                            )
        self.add_widget(self.title_label)

        self.meaning_label = Label(font_size=50,
                    color=(0, 1, 0, 1),
                    halign='left',
                    valign='top',
                    font_name=self.JAPANESE_FONT_NAME
                    )
        self.add_widget(self.meaning_label)

        self.sentence_label = Label(font_size=50,
                    color=(1, 1, 1, 1),
                    halign='left',
                    valign='top',
                    font_name=self.JAPANESE_FONT_NAME
                    )
        self.add_widget(self.sentence_label)

        self.index = -1
        self.words = []
        self.display_next_word()

    def normalize_pressure(self, pressure):
        print(pressure)
        # this might mean we are on a device whose pressure value is
        # incorrectly reported by SDL2, like recent iOS devices.
        if pressure == 0.0:
            return 1
        return dp(pressure * 10)

    def on_touch_down(self, touch):
        self.touch_down_x = touch.x
        self.touch_down_y = touch.y

    def on_touch_move(self, touch):
        pass

    def on_touch_up(self, touch):

        if touch.x - self.touch_down_x > self.SWIPE_WIDTH: # swiped right
            self.display_previous_word()
        elif self.touch_down_x - touch.x > self.SWIPE_WIDTH : # swiped left
            self.display_next_word()
        
        if self.meaning_label.x < touch.x < self.meaning_label.x + self.meaning_label.width:
            if self.meaning_label.y < touch.y < self.meaning_label.y + self.meaning_label.height:
                self.meaning_label.opacity = 100
    
    def display_next_word(self):
        self.index += 1

        if self.index < len(self.words):
            word = self.words[self.index]
        elif self.index == len(self.words):
            word = self.pickup_word()
            self.words.append(word)
            
        self.update_word_label(word)

    def display_previous_word(self):

        if self.index <= 0:
            pass
        else:
            self.index -= 1
            word = self.words[self.index]
            self.update_word_label(word)

    def update_word_label(self, word):
        
        self.title_label.text_size = (self.width - 20, None)
        self.title_label.text = word.title
        self.title_label.texture_update()
        self.title_label.size = self.title_label.texture_size
        self.title_label.text_size = self.title_label.texture_size
        self.title_label.pos = (10, self.height - self.title_label.height)
        
        self.meaning_label.text_size = (self.width - 20, None)
        self.meaning_label.text = word.meaning
        self.meaning_label.texture_update()
        self.meaning_label.size = self.meaning_label.texture_size
        self.meaning_label.text_size = self.meaning_label.texture_size
        self.meaning_label.pos = (10, self.height - self.title_label.height - self.meaning_label.height)  
        self.meaning_label.opacity = 0

        self.sentence_label.text_size = (self.width - 20, None)
        self.sentence_label.text = word.sentence
        self.sentence_label.texture_update()
        self.sentence_label.size = self.sentence_label.texture_size
        self.sentence_label.text_size = self.sentence_label.texture_size
        self.sentence_label.pos = (10, self.height - self.title_label.height - self.meaning_label.height - self.sentence_label.height)

    def pickup_word(self):

        while True:
            index = randint(3, len(self.word_matrix)-1)
            target_row = self.word_matrix[index]
            title = str(target_row[1])
            meaning = str(target_row[2])
            level = str(target_row[6])
            if title == "" or meaning == "" or level == "5":
                continue

            sentence = str(target_row[3])

            break

        word = Word(title, meaning, sentence)
        return word


class EverydayEnglishApp(App):
    #title = 'EverydayEnglish'
    #icon = 'icon.png'

    def build(self):

        self.icon = 'icon.png'
        self.title = 'EverydayEnglish'
        self.main_frame = EverydayEnglish()

        return self.main_frame

    def on_start(self):
        super().on_start()
        print("on_start")
        self.main_frame.prepare()

    def on_pause(self):
        return True



if __name__ == '__main__':
    EverydayEnglishApp().run()


