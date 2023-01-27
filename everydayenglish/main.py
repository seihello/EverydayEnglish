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
import csv

__version__ = '1.0'

import kivy
kivy.require('1.0.6')

class EverydayEnglish(ScreenManager):

    JAPANESE_FONT_NAME = 'ヒラギノ丸ゴ ProN W4.ttc'
    SWIPE_WIDTH = 50

    def prepare(self):
        #self.orientation = 'vertical'

        self.load_words()

        self.create_word_list_screen()
        self.create_word_screen()

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
        
        shuffle(self.words)
        # self.words = sorted(self.words, key=lambda w: w.level)

    def create_word_list_screen(self):
        self.word_list_screen = Screen(name="WordList")

        # self.top_bar = Widget()
        # self.top_bar.size = (self.width, self.height*0.1)
        # self.top_bar.pos = (0, self.height*0.9)
        # self.word_list_screen.add_widget(self.top_bar)

        self.word_list_bar_label = MyLabel()
        self.word_list_bar_label.text = "Word List"
        self.word_list_bar_label.size_hint_y = None
        self.word_list_bar_label.disabled_color      = (1, 1, 1, 1)
        self.word_list_bar_label.font_size  = 40
        self.word_list_bar_label.halign     = 'center'
        self.word_list_bar_label.valign     = 'middle'
        self.word_list_bar_label.font_name  = 'ヒラギノ丸ゴ ProN W4.ttc'
        self.word_list_bar_label.pos        = (0, self.height*0.94)
        self.word_list_bar_label.size       = (self.width, self.height*0.06)
        self.word_list_bar_label.text_size  = self.word_list_bar_label.size
        self.word_list_bar_label.background_color = (0.3, 0.3, 0.3, 0.95)

        self.word_list_scroll_view = ScrollView()
        self.word_list_scroll_view.size_hint = (1, None)
        self.word_list_scroll_view.size = (self.width, self.height)

        self.word_list_layout = Widget()
        self.word_list_layout.size = (self.width, self.height * 3)
        self.word_list_layout.size_hint_y = None
        #self.word_list_layout.spacing = 30
        #self.word_list_layout.bind(minimum_height=self.word_list_layout.setter('height'))
        #self.word_list_layout.orientation = 'vertical'
        self.word_list_layout.pos = (0, 0)
        
        displayed_rows = 500
        space = 20
        height_sum = 0

        self.word_list_labels = []
        for i in range(displayed_rows):
            word = self.words[i]
            word_label = WordLabel(self, word, i)           
            self.word_list_layout.add_widget(word_label.title_label)
            self.word_list_layout.add_widget(word_label.level_label)

            self.word_list_labels.append(word_label)
            height_sum += word_label.title_label.texture_size[1]
    
        self.word_list_layout.height = height_sum + space * displayed_rows

        y = self.word_list_layout.height
        for i in range(displayed_rows):
            y -= self.word_list_labels[i].title_label.texture_size[1]
            self.word_list_labels[i].set_y(y)

            y -= space / 2
            with self.word_list_layout.canvas:
                Color(1, 1, 1, 1)
                Rectangle(pos=(self.width*0.02, y), size=(self.width*0.96, 1))
            y -= space / 2

        self.word_list_scroll_view.add_widget(self.word_list_layout)
        self.word_list_screen.add_widget(self.word_list_scroll_view)
        self.add_widget(self.word_list_screen)

        self.word_list_screen.add_widget(self.word_list_bar_label)

    def create_word_screen(self):

        self.word_screen = Screen(name="Word")

        self.word_bar_label = Button()
        self.word_bar_label.text = "< Word List"
        self.word_bar_label.size_hint_y = None
        self.word_bar_label.color      = (0, 0.6, 1, 1)
        self.word_bar_label.font_size  = 40
        self.word_bar_label.halign     = 'left'
        self.word_bar_label.valign     = 'middle'
        self.word_bar_label.pos        = (0, self.height*0.94)
        self.word_bar_label.size       = (self.width, self.height*0.06)
        self.word_bar_label.text_size  = self.word_list_bar_label.size
        self.word_bar_label.background_normal = ''
        self.word_bar_label.background_disabled_normal = ''
        self.word_bar_label.background_down = ''
        self.word_bar_label.background_color = (0.3, 0.3, 0.3, 0.95)
        #self.word_bar_label.disabled_color = (0.3, 0.3, 0.3, 0.95)
        self.word_bar_label.on_release = self.back_to_word_list
        self.word_bar_label.padding_x = self.width*0.02
        #self.word_bar_label.on_press = self.change_back_to_word_list_button_color
        #self.word_bar_label.on_release = self.revert_back_to_word_list_button_color 
        
        self.word_screen.add_widget(self.word_bar_label)

        self.word_scroll_view = ScrollView()
        self.word_scroll_view.size_hint = (1, None)
        self.word_scroll_view.size = (self.width, self.height*0.94)

        self.word_layout = BoxLayout()
        self.word_layout.size = self.size
        self.word_layout.size_hint_y = None
        self.word_layout.spacing = 30
        self.word_layout.bind(minimum_height=self.word_layout.setter('height'))
        self.word_layout.orientation = 'vertical'
        self.word_layout.pos = (0, 0)

        print("make")
        self.title_label = Label(font_size=50,
                                 color=(0.9, 0.1, 0.2, 1),
                                 halign='left',
                                 valign='top',
                                 size_hint_y=None,
                                 width=self.width,
                                 padding_x=self.width*0.02,
                                 font_name=self.JAPANESE_FONT_NAME
                                 )
        self.word_layout.add_widget(self.title_label)

        self.meaning_label = Label(font_size=50,
                                   color=(0, 1, 0, 1),
                                   halign='left',
                                   valign='top',
                                   size_hint_y=None,
                                   width=self.width,
                                   padding_x=self.width*0.02,
                                   font_name=self.JAPANESE_FONT_NAME
                                   )
        self.word_layout.add_widget(self.meaning_label)

        self.sentence_label = Label(font_size=50,
                                    color=(1, 1, 1, 1),
                                    halign='left',
                                    valign='top',
                                    size_hint_y=None,
                                    width=self.width,
                                    padding_x=self.width*0.02,
                                    font_name=self.JAPANESE_FONT_NAME
                                    )
        self.word_layout.add_widget(self.sentence_label)

        self.word_scroll_view.add_widget(self.word_layout)
        self.word_screen.add_widget(self.word_scroll_view)
        self.add_widget(self.word_screen)



    def display_word(self, index):
        word = self.words[index]

        self.title_label.text_size = (self.width - 20, None)
        self.title_label.text = word.title
        self.title_label.texture_update()
        self.title_label.size = self.title_label.texture_size
        self.title_label.text_size = self.title_label.texture_size


        self.meaning_label.text_size = (self.width - 20, None)
        self.meaning_label.text = word.meaning
        self.meaning_label.texture_update()
        self.meaning_label.size = self.meaning_label.texture_size
        self.meaning_label.text_size = self.meaning_label.texture_size

        self.sentence_label.text_size = (self.width - 20, None)
        self.sentence_label.text = word.sentence
        self.sentence_label.texture_update()
        self.sentence_label.size = self.sentence_label.texture_size
        self.sentence_label.text_size = self.sentence_label.texture_size

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

