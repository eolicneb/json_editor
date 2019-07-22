import json
from pprint import pprint
from kivy.base import runTouchApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import *
from random import random

class Element(Label):
    def __init__(self, **kwargs):
        element = kwargs.pop('element', '')
        self.father = kwargs.pop('father', None)
        self.parent = kwargs.pop('parent', None)
        super().__init__(**kwargs)
        print(self.parent)
        if isinstance(element, tuple):
            self.label = element[0]
            self.what = element[1]
            if isinstance(self.what, list):
                self.text += f'{self.label}: [ .. ]'
            elif isinstance(self.what, dict):
                self.text += f'{self.label}: '+'{ ... }'
            else:
                self.text += f'{self.label}: {self.what}'
        elif isinstance(element, str):
            self.label, self.what = element, None
            self.text = self.label
        print(f'Element.text = {self.label}')
        self.size = self.texture_size
        with self.canvas:
            Color(random(), random(), random(), .7)
            Rectangle(size=self.size, pos=self.pos)
    def on_touch_up(self, touch):
        # if isinstance
        parent = self.parent
        for ch in parent.children:
            parent.remove_widget(ch)

class ShowObject(BoxLayout):
    def __init__(self, **kwargs):
        self.dict_ = kwargs.pop('dict', {})
        super().__init__(**kwargs)
        self.load(self.dict_)
    def load(self, dict_):
        self.dict_ = dict_
        for ch in self.children:
            self.remove_widget(ch)
        for key, val in dict_.items():
            self.add_widget(Element(element=(key, val), parent=self))
        print(f'Object has {len(self.children)} elements')


class Dict_editor(object):
    def __init__(self, dict_):
        self.dict = dict_
    
dic = {}
with open('json.json', 'r') as jsonfile:
    # dic = jsonfile.readlines()
    dic = json.load(jsonfile)
    pprint(dic['parameters'])
    with open('json_new.json', 'w') as exitfile:
        dic.update({'second_parameters': dic['parameters']})
        json.dump(dic, exitfile,indent=2)

show = ShowObject(dict=dic, orientation='vertical')
runTouchApp(show)