from word import Word, WordLabel
from random import randint, shuffle
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Point, GraphicException
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from operator import itemgetter
from gui import MyLabel
from kivy.properties import ObjectProperty
import csv

__version__ = '1.0'

import kivy
kivy.require('2.1.0')

# from kivy.lang import Builder
# Builder.load_file('everydayenglish.kv')

class EverydayEnglish(ScreenManager):

    word_list_widget = ObjectProperty(None)
    word_title_label = ObjectProperty(None)
    word_meaning_label = ObjectProperty(None)
    word_sentence_label = ObjectProperty(None)
    word_layout = ObjectProperty(None)

    JAPANESE_FONT_NAME = 'ヒラギノ丸ゴ ProN W4.ttc'
    SWIPE_WIDTH = 50

    def prepare(self):

        self.load_words()

        self.create_word_list_screen()

        # Initial screen
        self.current = "WordList"

    # Load words from the csv file to make a list
    def load_words(self):
        with open('english.csv') as f:
            reader = csv.reader(f)
            self.word_matrix = [row for row in reader]
        
        self.words = []
        for i in range(3, len(self.word_matrix)-1):
            word = Word(self.word_matrix[i][1], self.word_matrix[i][2], self.word_matrix[i][3], self.word_matrix[i][6])
            if word.title != 'None' and word.title != '':
                self.words.append(word)

    def create_word_list_screen(self):

        shuffle(self.words)
        # self.words = sorted(self.words, key=lambda w: w.level)

        displayed_rows = 100
        space = 20
        height_sum = 0

        self.word_list_labels = []
        for i in range(displayed_rows):
            word = self.words[i]
            word_label = WordLabel(self, word, i)           
            self.word_list_widget.add_widget(word_label.title_label)
            self.word_list_widget.add_widget(word_label.level_label)

            self.word_list_labels.append(word_label)
            height_sum += word_label.title_label.texture_size[1]
    
        self.word_list_widget.height = height_sum + space * displayed_rows
    
        y = self.word_list_widget.height
        for i in range(displayed_rows):
            y -= self.word_list_labels[i].title_label.texture_size[1]
            self.word_list_labels[i].set_y(y)

            y -= space / 2
            with self.word_list_widget.canvas:
                Color(1, 1, 1, 1)
                Rectangle(pos=(self.width*0.02, y), size=(self.width*0.96, 1))
            y -= space / 2


    def display_word(self, index):
        word = self.words[index]

        self.word_title_label.text_size = (self.width - 20, None)
        self.word_title_label.text = word.title
        self.word_title_label.texture_update()
        self.word_title_label.size = self.word_title_label.texture_size
        self.word_title_label.text_size = self.word_title_label.texture_size

        self.word_meaning_label.text_size = (self.width - 20, None)
        self.word_meaning_label.text = word.meaning
        self.word_meaning_label.texture_update()
        self.word_meaning_label.size = self.word_meaning_label.texture_size
        self.word_meaning_label.text_size = self.word_meaning_label.texture_size

        self.word_sentence_label.text_size = (self.width - 20, None)
        self.word_sentence_label.text = word.sentence
        self.word_sentence_label.texture_update()
        self.word_sentence_label.size = self.word_sentence_label.texture_size
        self.word_sentence_label.text_size = self.word_sentence_label.texture_size

        self.transition.direction = "left"
        self.current = "Word"
    
    def back_to_word_list(self):
        self.transition.direction = "right"
        self.current = "WordList"

class EverydayEnglishApp(App):

    # title = 'EverydayEnglish'
    # icon = 'icon.png'

    def build(self):
        self.icon = 'icon.png'
        self.title = 'EverydayEnglish'
        self.main_frame = EverydayEnglish()

        return self.main_frame

    def on_start(self):
        super().on_start()
        self.main_frame.prepare()

    def on_pause(self):
        return True

if __name__ == '__main__':
    EverydayEnglishApp().run()

