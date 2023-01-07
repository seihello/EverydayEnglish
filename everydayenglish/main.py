from word import Word
from math import sqrt
from random import randint
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle, Point, GraphicException
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
import csv

__version__ = '1.0'

import kivy
kivy.require('1.0.6')


class EverydayEnglish(BoxLayout):

    JAPANESE_FONT_NAME = 'ヒラギノ丸ゴ ProN W4.ttc'

    def prepare(self):

        self.orientation = 'vertical'

        with open('english.csv') as f:
            reader = csv.reader(f)
            self.word_list = [row for row in reader]

        title, meaning, sentences = self.pickup_word()

        self.title_label = Label(text=title,
                                 font_size=70,
                                 color=(1, 0, 0, 1),
                                 halign='left',
                                 valign='top',
                                 text_size=(self.width*0.9, self.height/3),
                                 font_name=self.JAPANESE_FONT_NAME
                                 )
        self.add_widget(self.title_label)

        self.meaning_label = Label(text=meaning,
                                   font_size=50,
                                   halign='left',
                                   valign='top',
                                   text_size=(self.width*0.9, self.height/3),
                                   color=(0, 1, 0, 1),
                                   font_name=self.JAPANESE_FONT_NAME
                                   )
        self.add_widget(self.meaning_label)

        self.sentence_label = Label(text=sentences,
                                    font_size=50,
                                    halign='left',
                                    valign='top',
                                    text_size=(self.width*0.9, self.height/3),
                                    color=(1, 1, 1, 1),
                                    font_name=self.JAPANESE_FONT_NAME
                                    )
        self.add_widget(self.sentence_label)

    def normalize_pressure(self, pressure):
        print(pressure)
        # this might mean we are on a device whose pressure value is
        # incorrectly reported by SDL2, like recent iOS devices.
        if pressure == 0.0:
            return 1
        return dp(pressure * 10)

    def on_touch_down(self, touch):
        pass

    def on_touch_move(self, touch):
        pass

    def on_touch_up(self, touch):
        self.update_word_label()

    def update_word_label(self):
        title, meaning, sentences = self.pickup_word()
        self.title_label.text = title
        self.meaning_label.text = meaning
        self.sentence_label.text = sentences

    def pickup_word(self):

        title = ""
        meaning = ""
        sentences = ""

        while True:
            index = randint(3, len(self.word_list)-1)
            target_row = self.word_list[index]
            title = str(target_row[1])
            meaning = str(target_row[2])
            level = str(target_row[6])
            if title == "" or meaning == "" or level == "5":
                continue

            sentences = str(target_row[3])

            break

        return title, meaning, sentences


class EverydayEnglishApp(App):
    title = 'EverydayEnglish'
    icon = 'icon.png'

    def build(self):

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
