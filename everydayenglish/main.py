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
        #self.create_word_screen()

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
            word_label = WordLabel(self, word.title)            
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

    def on_click_word(self):
        pass

    # def on_touch_down(self, touch):
    #     self.touch_down_x = touch.x
    #     self.touch_down_y = touch.y

    #     self.scroll_start_y = touch.y

    # def on_touch_up(self, touch):
    #     if abs(touch.y - self.touch_down_y) < self.SWIPE_WIDTH * 2:
    #         # swiped right
    #         if touch.x - self.touch_down_x > self.SWIPE_WIDTH:
    #             self.display_previous_word()
    #         # swiped left
    #         elif self.touch_down_x - touch.x > self.SWIPE_WIDTH:
    #             self.display_next_word()
    #         # just touched
    #         else:
    #             self.meaning_label.opacity = 100
    
    # def on_touch_move(self, touch):
    #     if self.scrollable:
    #         dy = touch.y - self.scroll_start_y

    #         if self.sentence_label.y + dy > 0:
    #             dy = self.sentence_label.y * -1
    #         elif self.title_label.y + self.title_label.texture_size[1] + dy < self.height:
    #             dy = self.height - (self.title_label.y + self.title_label.texture_size[1])

    #         self.title_label.y += dy
    #         self.meaning_label.y += dy
    #         self.sentence_label.y += dy

    #     self.scroll_start_y = touch.y

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
        self.meaning_label.pos = (
            10, self.height - self.title_label.height - self.meaning_label.height)
        self.meaning_label.opacity = 0

        self.sentence_label.text_size = (self.width - 20, None)
        self.sentence_label.text = word.sentence
        self.sentence_label.texture_update()
        self.sentence_label.size = self.sentence_label.texture_size
        self.sentence_label.text_size = self.sentence_label.texture_size
        self.sentence_label.pos = (10, self.height - self.title_label.height -
                                   self.meaning_label.height - self.sentence_label.height)
        
        if self.sentence_label.y < 0:
            self.scrollable = True
        else:
            self.scrollable = False
        

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
