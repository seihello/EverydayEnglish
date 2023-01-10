from word import Word
from random import randint
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Point, GraphicException
from kivy.uix.label import Label
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

        self.sentence_label = Label(font_size=80,
                                    color=(1, 1, 1, 1),
                                    halign='left',
                                    valign='top',
                                    font_name=self.JAPANESE_FONT_NAME
                                    )
        self.add_widget(self.sentence_label)

        self.index = -1
        self.words = []
        self.display_next_word()

    def on_touch_down(self, touch):
        self.touch_down_x = touch.x
        self.touch_down_y = touch.y

        self.scroll_start_y = touch.y

    def on_touch_up(self, touch):
        if abs(touch.y - self.touch_down_y) < self.SWIPE_WIDTH:
            # swiped right
            if touch.x - self.touch_down_x > self.SWIPE_WIDTH:
                self.display_previous_word()
            # swiped left
            elif self.touch_down_x - touch.x > self.SWIPE_WIDTH:
                self.display_next_word()
            # just touched
            else:
                self.meaning_label.opacity = 100
    
    def on_touch_move(self, touch):
        if self.scrollable:
            dy = touch.y - self.scroll_start_y

            if self.sentence_label.y + dy > 0:
                dy = self.sentence_label.y * -1
            elif self.title_label.y + self.title_label.texture_size[1] + dy < self.height:
                dy = self.height - (self.title_label.y + self.title_label.texture_size[1])

            print(dy)
            self.title_label.y += dy
            self.meaning_label.y += dy
            self.sentence_label.y += dy

        self.scroll_start_y = touch.y

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
            print("Sticking out")
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
