from kivy.uix.button import Button

class MyLabel(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.disabled = True
        self.background_normal = ''
        self.background_disabled_normal = ''
        self.background_color = (0, 0, 0, 1)
