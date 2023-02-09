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
    word_list_top_bar = ObjectProperty(None)
    word_list_screen = ObjectProperty(None)
    filter_widget = ObjectProperty(None)
    level1 = ObjectProperty(None)
    level2 = ObjectProperty(None)
    level3 = ObjectProperty(None)
    level4 = ObjectProperty(None)
    level5 = ObjectProperty(None)

    JAPANESE_FONT_NAME = 'ヒラギノ丸ゴ ProN W4.ttc'
    SWIPE_WIDTH = 50

    def prepare(self):

        self.valid_levels = [False, True, True, True, True, True]
        self.level_buttons = [self.level1, self.level2, self.level3, self.level4, self.level5]

        self.load_words()

        self.create_word_list_screen()

        # Initial screen
        self.current = "WordList"

        self.word_list_screen.remove_widget(self.filter_widget)

        

    # Load words from the csv file to make a list
    def load_words(self):
        with open('english.csv') as f:
            reader = csv.reader(f)
            self.word_matrix = [row for row in reader]
        
        self.words = []
        for i in range(3, len(self.word_matrix)-1):
            try:
                title = self.word_matrix[i][1]
                meaning = self.word_matrix[i][2]
                sentence = self.word_matrix[i][3]
                level = int(self.word_matrix[i][6])
            except ValueError:
                pass
            else:
                if title != 'None' and title != '':
                    self.words.append(Word(title, meaning, sentence, level))

    def create_word_list_screen(self):

        self.word_list_widget.canvas.clear()

        shuffle(self.words)
        # self.words = sorted(self.words, key=lambda w: w.level)

        displayed_rows = 200
        space = 20
        height_sum = 0

        self.word_list_labels = []
        count = 0
        for i in range(len(self.words)):
            word = self.words[i]

            if type(word.level) is not int or not self.valid_levels[word.level]:
                continue
            
            word_label = WordLabel(self, word, i)           
            self.word_list_widget.add_widget(word_label.title_label)
            self.word_list_widget.add_widget(word_label.level_label)

            self.word_list_labels.append(word_label)
            height_sum += word_label.title_label.texture_size[1]

            count += 1
            if count >= displayed_rows:
                break
    
        self.word_list_widget.height = height_sum + space * displayed_rows + self.word_list_top_bar.height
    
        y = self.word_list_widget.height
        for i in range(displayed_rows):
            y -= self.word_list_labels[i].title_label.texture_size[1]
            self.word_list_labels[i].set_y(y - self.word_list_top_bar.height)

            y -= space / 2
            with self.word_list_widget.canvas:
                Color(1, 1, 1, 1)
                Rectangle(pos=(self.width*0.02, y - self.word_list_top_bar.height), size=(self.width*0.96, 1))
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
    
    def show_filter(self):
        self.word_list_screen.add_widget(self.filter_widget)

    def on_release_level1(self):
        self.on_release_level(1)
    def on_release_level2(self):
        self.on_release_level(2)
    def on_release_level3(self):
        self.on_release_level(3)
    def on_release_level4(self):
        self.on_release_level(4)
    def on_release_level5(self):
        self.on_release_level(5)
    
    def on_release_level(self, level):
        if self.valid_levels[level]:
            self.level_buttons[level-1].background_color = (.3, .3, .3, .95)
            self.valid_levels[level] = False
        else:
            self.level_buttons[level-1].background_color = (0, 0, 1, 1)
            self.valid_levels[level] = True

    def on_release_OK_button(self):
        self.word_list_screen.remove_widget(self.filter_widget)
        self.create_word_list_screen()


    



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

