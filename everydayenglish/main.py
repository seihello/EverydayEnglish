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

    def prepare(self):

        self.orientation = 'vertical'

        with open('english.csv') as f:
            reader = csv.reader(f)
            self.word_list = [row for row in reader]

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

        self.update_word_label()

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

        self.title_label.text_size = (self.width - 20, None)
        self.title_label.text = title
        self.title_label.texture_update()
        self.title_label.size = self.title_label.texture_size
        self.title_label.text_size = self.title_label.texture_size
        self.title_label.pos = (10, self.height - self.title_label.height)
        
        self.meaning_label.text_size = (self.width - 20, None)
        self.meaning_label.text = meaning
        self.meaning_label.texture_update()
        self.meaning_label.size = self.meaning_label.texture_size
        self.meaning_label.text_size = self.meaning_label.texture_size
        self.meaning_label.pos = (10, self.height - self.title_label.height - self.meaning_label.height)  

        self.sentence_label.text_size = (self.width - 20, None)
        self.sentence_label.text = sentences
        self.sentence_label.texture_update()
        self.sentence_label.size = self.sentence_label.texture_size
        self.sentence_label.text_size = self.sentence_label.texture_size
        self.sentence_label.pos = (10, self.height - self.title_label.height - self.meaning_label.height - self.sentence_label.height)



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
