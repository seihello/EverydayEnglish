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

    def create_word_list_screen(self):
        self.word_list_screen = Screen(name="WordList")

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
        
        displayed_rows = 100
        space = 20
        height_sum = 0

        self.word_list_labels = []
        for i in range(displayed_rows):
            word = self.words[i]
            word_label = WordLabel(self, word.title, i)           
            self.word_list_layout.add_widget(word_label)

            self.word_list_labels.append(word_label)
            height_sum += word_label.texture_size[1]

            # line = Widget(size=(self.width, 100))
            # with self.word_list_layout.canvas:
            #     Color(1, 1, 1, 1)
            #     Rectangle(pos=(0, 0), size=(100, 10))
            # line.size_hint = (1, None)
            # self.word_list_layout.add_widget(line)
    
        self.word_list_layout.height = height_sum + space * displayed_rows

        y = self.word_list_layout.height
        for i in range(displayed_rows):
            y -= self.word_list_labels[i].texture_size[1]
            self.word_list_labels[i].pos = (0, y)

            y -= space / 2
            with self.word_list_layout.canvas:
                Color(1, 1, 1, 1)
                Rectangle(pos=(0, y), size=(self.width, 3))
            y -= space / 2

        # with self.word_list_layout.canvas:
        #     Color(1, 1, 1, 1)
        #     Rectangle(size=(self.width, 3))
        #     Color(1, 0, 1, 1)
        #     Rectangle(pos=(0, 900),size=(self.width, 3))

        self.word_list_scroll_view.add_widget(self.word_list_layout)
        self.word_list_screen.add_widget(self.word_list_scroll_view)
        self.add_widget(self.word_list_screen)

    def create_word_screen(self):

        self.word_screen = Screen(name="Word")

        self.word_scroll_view = ScrollView()
        self.word_scroll_view.size_hint = (1, None)
        self.word_scroll_view.size = (self.width, self.height)

        self.word_layout = BoxLayout()
        self.word_layout.size = self.size
        self.word_layout.size_hint_y = None
        self.word_layout.spacing = 30
        self.word_layout.bind(minimum_height=self.word_layout.setter('height'))
        self.word_layout.orientation = 'vertical'
        self.word_layout.pos = (0, 0)


        self.title_label = Label(font_size=70,
                                 color=(1, 0, 0, 1),
                                 halign='left',
                                 valign='top',
                                 size_hint_y=None,
                                 width=self.width,
                                 font_name=self.JAPANESE_FONT_NAME
                                 )
        self.word_layout.add_widget(self.title_label)

        self.meaning_label = Label(font_size=50,
                                   color=(0, 1, 0, 1),
                                   halign='left',
                                   valign='top',
                                   size_hint_y=None,
                                   width=self.width,
                                   font_name=self.JAPANESE_FONT_NAME
                                   )
        self.word_layout.add_widget(self.meaning_label)

        self.sentence_label = Label(font_size=50,
                                    color=(1, 1, 1, 1),
                                    halign='left',
                                    valign='top',
                                    size_hint_y=None,
                                    width=self.width,
                                    font_name=self.JAPANESE_FONT_NAME
                                    )
        self.word_layout.add_widget(self.sentence_label)

        self.word_scroll_view.add_widget(self.word_layout)
        self.word_screen.add_widget(self.word_scroll_view)
        self.add_widget(self.word_screen)

    def display_word(self, index):
        word = self.words[index]
        print(word.title)

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
