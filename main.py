from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.utils import platform
from kivy.properties import StringProperty,NumericProperty
from kivy.uix.image import Image
from kivy.animation import Animation
from random import randint

class MenuScreen(Screen):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

class GameScreen(Screen):
  c_click = StringProperty()
  points = NumericProperty()
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.c_click = '0'

  def clicker(self):
    self.c_click = str(int(self.c_click) +1)
  def on_enter(self, *args):
    self.ids.planet.new_planet
    return super().on_enter(*args)


class Witch(Image):
  is_animation=False
  hp = None
  witch = None
  witch_index = 0

  def on_touch_down(self, touch):
    if self.collide_point(*touch.pos) and not self.is_animation:
      self.parent.parent.parent.points +=1
      self.hp -=1
      if self.hp <=0:
        anim = Animation(opacity = 0, d=1)
        anim.start(self)
        self.new_planet()

      x= self.x
      y= self.y
      anim = Animation(x=x, y=y-5, d=0.03) + Animation(x=x, y=y, d=0.03)
      anim.start(self)
      self.is_animation = True

      anim.on_complete = lambda *arg: setattr(self, "is_animation", False)

    return super().on_touch_down(touch)

  def new_planet(self):
    self.planet = app.LEVELS[randint(0,len(app.LEVELS)-1)]
    self.source = app.PLANETS[self.planet]['source']
    self.hp = app.PLANETS[self.hp]['source']
    anim = Animation(opacity = 1, d=1)
    anim.start(self)

class MainApp(App):
  def build(self):
    sm = ScreenManager()
    sm.add_widget(MenuScreen(name = 'menu'))
    sm.add_widget(GameScreen(name = 'game'))
    return sm

if platform != 'android':
  Window.size = (400,800)
  Window.left = 750
  Window.top = 100
  
app= MainApp()
app.run

  # PLANETS = {
#         'Mercury': {"source": 'assets/planets/1.png', 'hp': 10},
#         'Venus': {"source": 'assets/planets/2.png', 'hp': 20},
#         'Earth': {"source": 'assets/planets/3.png', 'hp': 30},
#         'Mars': {"source": 'assets/planets/4.png', 'hp': 40},
#         'Jupiter': {"source": 'assets/planets/5.png', 'hp': 50},
#         'Saturn': {"source": 'assets/planets/6.png', 'hp': 60},
#         'Uranus': {"source": 'assets/planets/7.png', 'hp': 80}
# }
#   # LEVELS = ['Mercury', 'Venus', 'Earth', 'Mars',
  #             'Jupiter', 'Saturn', 'Uranus', 'Neptune']
