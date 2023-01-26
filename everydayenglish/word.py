from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle

class Word:
    def __init__(self, title, meaning, sentence, level) -> None:
        self.title = title
        self.meaning = meaning
        self.sentence = sentence
        self.level = level

class WordLabel(Label):
    def __init__(self, app, title, index) -> None:
        super().__init__()
        self.app = app
        self.index = index

        self.color = (1, 1, 1, 1)
        self.font_size = 40
        self.halign = 'left'
        self.valign = 'top'
        self.font_name = 'ヒラギノ丸ゴ ProN W4.ttc'

        self.font_size = 50
        self.size_hint_y = None
        self.text = title
        #self.width = app.width*0.9
        self.text_size = (app.width*0.92, None)
        self.texture_update()
        self.size = self.texture_size
        

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            self.app.display_word(self.index)
    