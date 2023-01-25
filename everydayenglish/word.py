from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle

class Word:
    def __init__(self, title, meaning, sentence, level) -> None:
        self.title = title
        self.meaning = meaning
        self.sentence = sentence
        self.level = level

class WordLabel(Label):
    def __init__(self, app, title) -> None:
        super().__init__()
        self.app = app
        self.color = (1, 1, 1, 1)
        self.font_size = 40
        self.halign = 'left'
        self.valign = 'top'
        self.font_name = 'ヒラギノ丸ゴ ProN W4.ttc'

        self.size_hint_y = None
        self.text = title
        self.text_size = (app.width-100, None)
        self.texture_update()
        self.size = self.texture_size
        self.text_size = self.texture_size

    def on_touch_down(self, touch):
        self.app.on_click_word()
    