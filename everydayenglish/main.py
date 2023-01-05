__version__ = '1.0'

import kivy
kivy.require('1.0.6')

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle, Point, GraphicException
from kivy.metrics import dp
from random import random
from math import sqrt

from word import Word
import random

def calculate_points(x1, y1, x2, y2, steps=5):
    dx = x2 - x1
    dy = y2 - y1
    dist = sqrt(dx * dx + dy * dy)
    if dist < steps:
        return
    o = []
    m = dist / steps
    for i in range(1, int(m)):
        mi = i / m
        lastx = x1 + dx * mi
        lasty = y1 + dy * mi
        o.extend([lastx, lasty])
    return o


class Touchtracer(FloatLayout):

    def __init__(self, word_list) -> None:
        super().__init__()

        index = random.randint(0, len(word_list))
        word = word_list[index]

        title_label = Label(text=word.title,
                                font_size='70',
                                color=(1,0,0,1),
                                pos_hint={'y':0.1}
                              )
        self.add_widget(title_label)

        meaning_label = Label(text=word.meaning,
                      font_size='50',
                      color=(0,1,0,1),
                      pos=(10, 10),
                      font_name = '/System/Library/Fonts/ヒラギノ丸ゴ ProN W4.ttc'
                      )
        self.add_widget(meaning_label)

        sentence_label = Label(text=word.sentence,
                      font_size='50',
                      color=(0,1,0,1),
                      pos=(10, 10),
                      pos_hint={'y':-0.1}
                      )
        self.add_widget(sentence_label)


    def normalize_pressure(self, pressure):
        print(pressure)
        # this might mean we are on a device whose pressure value is
        # incorrectly reported by SDL2, like recent iOS devices.
        if pressure == 0.0:
            return 1
        return dp(pressure * 10)

    def on_touch_down(self, touch):
        win = self.get_parent_window()
        ud = touch.ud
        ud['group'] = g = str(touch.uid)
        pointsize = 5
        print(touch.profile)
        if 'pressure' in touch.profile:
            ud['pressure'] = touch.pressure
            pointsize = self.normalize_pressure(touch.pressure)
        ud['color'] = random()

        with self.canvas:
            Color(ud['color'], 1, 1, mode='hsv', group=g)
            ud['lines'] = [
                Rectangle(pos=(touch.x, 0), size=(1, win.height), group=g),
                Rectangle(pos=(0, touch.y), size=(win.width, 1), group=g),
                Point(points=(touch.x, touch.y), source='particle.png',
                      pointsize=pointsize, group=g)]

        ud['label'] = Label(size_hint=(None, None))
        self.update_touch_label(ud['label'], touch)
        self.add_widget(ud['label'])
        touch.grab(self)
        return True

    def on_touch_move(self, touch):
        if touch.grab_current is not self:
            return
        ud = touch.ud
        ud['lines'][0].pos = touch.x, 0
        ud['lines'][1].pos = 0, touch.y

        index = -1

        while True:
            try:
                points = ud['lines'][index].points
                oldx, oldy = points[-2], points[-1]
                break
            except IndexError:
                index -= 1

        points = calculate_points(oldx, oldy, touch.x, touch.y)

        # if pressure changed create a new point instruction
        if 'pressure' in ud:
            old_pressure = ud['pressure']
            if (
                not old_pressure
                or not .99 < (touch.pressure / old_pressure) < 1.01
            ):
                g = ud['group']
                pointsize = self.normalize_pressure(touch.pressure)
                with self.canvas:
                    Color(ud['color'], 1, 1, mode='hsv', group=g)
                    ud['lines'].append(
                        Point(points=(), source='particle.png',
                              pointsize=pointsize, group=g))

        if points:
            try:
                lp = ud['lines'][-1].add_point
                for idx in range(0, len(points), 2):
                    lp(points[idx], points[idx + 1])
            except GraphicException:
                pass

        ud['label'].pos = touch.pos
        import time
        t = int(time.time())
        if t not in ud:
            ud[t] = 1
        else:
            ud[t] += 1
        self.update_touch_label(ud['label'], touch)

    def on_touch_up(self, touch):
        if touch.grab_current is not self:
            return
        touch.ungrab(self)
        ud = touch.ud
        self.canvas.remove_group(ud['group'])
        self.remove_widget(ud['label'])

    def update_touch_label(self, label, touch):
        label.text = 'ID: %s\nPos: (%d, %d)\nClass: %s' % (
            touch.id, touch.x, touch.y, touch.__class__.__name__)
        label.texture_update()
        label.pos = touch.pos
        label.size = label.texture_size[0] + 20, label.texture_size[1] + 20


class TouchtracerApp(App):
    title = 'Touchtracer'
    icon = 'icon.png'

    def build(self):

        word_list = self.load_word()

        return Touchtracer(word_list)

    def on_pause(self):
        return True

    def load_word(self):
        word_list = [
                        Word("euphemism", "婉曲表現", "Pass away is a euphemism for die."),
                        Word("orthodox", "正統派の、伝統的な", "I am not a very orthodox kind of counsellor."),
                        Word("red flag", "怪しい、危険信号", "The fact that he tries to hide his text messages from you is a bit of a red flag.")
                    ]

        return word_list

if __name__ == '__main__':
    TouchtracerApp().run()
