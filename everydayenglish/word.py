from gui import MyLabel
from kivy.graphics import Color, Rectangle

class Word:
    def __init__(self, title, meaning, sentence, level) -> None:
        self.title = title
        self.meaning = meaning
        self.sentence = sentence
        self.level = level

class WordLabel():

    COLORS = ((0.1, 0.1, 0.1, 1), (1, 0.2, 0.2, 1), (1, 0.6, 0, 1), (0, 0.8, 0.2, 1), (0, 0.5, 0.8, 1), (0.4, 0.1, 1, 1))

    def __init__(self, app, word, index) -> None:

        self.app = app
        self.word = word
        self.index = index

        self.title_label            = MyLabel()
        self.title_label.disabled_color      = (1, 1, 1, 1)
        self.title_label.font_size  = 40
        self.title_label.halign     = 'left'
        self.title_label.valign     = 'middle'
        self.title_label.font_name  = 'ヒラギノ丸ゴ ProN W4.ttc'
        self.title_label.x          = app.width*0.04
        self.title_label.disabled = False

        self.title_label.size_hint_y    = None
        self.title_label.text_size      = (app.width*0.80, None)

        self.title_label.text       = word.title
        self.title_label.texture_update()
        self.title_label.size       = self.title_label.texture_size

        self.title_label.on_release = self.on_touch_up

        self.level_label            = MyLabel()
        self.level_label.disabled_color      = (1, 1, 1, 1)
        self.level_label.font_size  = 32
        self.level_label.halign     = 'center'
        self.level_label.valign     = 'middle'
        self.level_label.font_name  = 'ヒラギノ丸ゴ ProN W4.ttc'
        self.level_label.x          = app.width*0.88

        #self.level_label.size_hint_y    = None
        self.level_label.text_size      = (app.width*0.08, None)

        self.level_label.text       = word.level
        self.level_label.texture_update()
        self.level_label.size       = self.level_label.texture_size

        if "0" <= word.level and word.level <= "5":
            self.level_label.background_color = WordLabel.COLORS[int(word.level)]
        
    def set_y(self, y):
        self.title_label.y = y
        self.level_label.y = y

    def on_touch_up(self):
        self.app.display_word(self.index)
    