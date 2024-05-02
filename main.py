from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.window import Window
from kivy.utils import platform

from kivy.properties import StringProperty, NumericProperty
from kivy.uix.image import Image
from kivy.animation import Animation
from random import randint, choice, shuffle
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.base import stopTouchApp
from kivy.storage.jsonstore import JsonStore
# import os


class MenuScreen(Screen):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def on_enter(self, *args):
    app.save_prog


class GameScreen(Screen):
  points = NumericProperty(0)

  def __init__(self, **kw):
    super().__init__(**kw)
    popup = Popup(title='Заголовок вікна',
                  content=Label(text='Текст Popup'))
    popup.open()

  def on_enter(self, *args):
    self.ids.witch.new_witch()
    return super().on_enter(*args)


class Witch(Image):
  is_anim= False
  hp = None
  witch = None
  witch_index = 0
  points = 0
  mult = 1
  def on_touch_down(self, touch):
    if self.collide_point(*touch.pos) and not self.is_anim:
        
      self.parent.parent.parent.points += (1*self.mult)
      self.points += (1*self.mult)
      self.hp -= 1

      if self.hp <= 0:
          self.break_witch()
          app.storage.put('progress', witch=self.witch)
      else:
          x = self.x
          y = self.y
          size =self.size.copy()
          anim = Animation(
              size=(size[0]*1.2, size[1]*1.2), t='out_back', d=0.1) + Animation(size=(size[0], size[1]), d=.1)
          anim.start(self)
          self.is_anim = True
          anim.on_complete = lambda *arg: setattr(self, 'is_anim', False)

    return super().on_touch_down(touch)

  def new_witch(self, *args):
    Witch.witch = self.witch =app.LEVELS[randint(0,len(app.LEVELS)-1)]
    # self.witch = app.LEVELS[randint(0, len(app.LEVELS) - 1)]
    self.source = app.WITCHES[self.witch]['source']
    self.hp = app.WITCHES[self.witch]['hp']
    self.size = app.WITCHES[self.witch]['size']
    size = self.size.copy()
    self.size = size[0], size[1]
    self.center = self.parent.center
    anim = Animation(opacity=1, d=0.3)
    anim &= Animation(
      size=(self.size[0] / 1.5, self.size[1] / 1.5), d=.2, t='out_back')
    anim &= Animation(center=self.parent.center, d=.3)
    anim.start(self)
    anim.on_complete = lambda *arg: setattr(self, "is_anim", False)

  def break_witch(self):
    self.is_anim = True
    anim = Animation(size=(self.size[0] * 2, self.size[1] * 2), d=.2)
    anim &= Animation(center=self.parent.center, d=.2)
    anim &= Animation(opacity=0, d=0.3)

    anim.start(self)
    anim.on_complete = Clock.schedule_once(self.new_witch, .5)

  # def build(self):
  #   sm = ScreenManager()
  #   sm.add_widget(MenuScreen(name='menu'))
  #   sm.add_widget(GameScreen(name='game'))
  #   return sm


class MainApp(App):
  storage = None
  LEVELS = ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus']

  WITCHES = {
      'Mercury': {"source": 'assets/witches/1.png', 'hp': 20, "size": ("200dp", "200dp")},
      'Venus': {"source": 'assets/witches/2.png', 'hp': 20, "size": ("200dp", "200dp")},
      'Earth': {"source": 'assets/witches/3.png', 'hp': 30, "size": ("200dp", "200dp")},
      'Mars': {"source": 'assets/witches/4.png', 'hp': 40, "size": ("200dp", "200dp")},
      'Jupiter': {"source": 'assets/witches/5.png', 'hp': 50, "size": ("200dp", "200dp")},
      'Saturn': {"source": 'assets/witches/6.png', 'hp': 60, "size": ("200dp", "200dp")},
      'Uranus': {"source": 'assets/witches/7.png', 'hp': 80, "size": ("200dp", "200dp")}

  }  #Priklad v komenti

  def save_prog(self):
    app.storaage.put('progress',
                     witch=Witch.witch,
                     hp=Witch.hp,
                     witch_index=Witch.witch_index,
                     mult=Witch.mult,
                     points=Witch.points)

  def build(self):
    global storage
    self.storage = JsonStore(self.user_data_dir + "storage.json")
    storage = self.storage
    sm = ScreenManager(transition=FadeTransition(duration=1))
    sm.add_widget(MenuScreen(name='menu'))
    sm.add_widget(GameScreen(name='game'))
    return sm

  def load_prog(self):
    return self.storage.get("progress")


if platform != 'android':
  Window.size = (400, 800)
  Window.left = 750
  Window.top = 100

app = MainApp()
app.run()

# witchS = {
#         'Mercury': {"source": 'assets/witchs/1.png', 'hp': 10},
#         'Venus': {"source": 'assets/witchs/2.png', 'hp': 20},
#         'Earth': {"source": 'assets/witchs/3.png', 'hp': 30},
#         'Mars': {"source": 'assets/witchs/4.png', 'hp': 40},
#         'Jupiter': {"source": 'assets/witchs/5.png', 'hp': 50},
#         'Saturn': {"source": 'assets/witchs/6.png', 'hp': 60},
#         'Uranus': {"source": 'assets/witchs/7.png', 'hp': 80}
# }
#   # LEVELS = ['Mercury', 'Venus', 'Earth', 'Mars',
#             'Jupiter', 'Saturn', 'Uranus', 'Neptune']
