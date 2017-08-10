#!/usr/bin/python python
# -*- coding: utf-8 -*-

#import subprocess
import os  # für den Dateibrowser
#import time
#from threading import Timer    # für den timer 2, 5 oder 10s
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
#from kivy.uix.floatlayout import FloatLayout
#from kivy.properties import ObjectProperty
#from kivy.uix.popup import Popup

#from kivy.core.window import Window
#from settingscanbus import settings_can , settings_rekord ,settings_play
#from kivy.uix.settings import SettingsWithSidebar

import canbusstatus


class Bildschirmverwalter(ScreenManager): pass
class Hauptbildschirm(Screen): pass
class Wiedergabe(Screen): pass
class Aufzeichnen(Screen): pass

# Alle im der KV Datei verwendeten Klassen müssen vor dem Laden definiert sein
# Die Klassen werden dann beim Laden aufgerufen
#Kivy_Beschreibung_laden = Builder.load_file('canbusanzeige.kv')

class programm(App):
    # ob can0 existiert True oder False
    # self.can0_exist=can0_exist
    title = 'Canbus Rekorder'
    #    icon = 'canbus2.png'
    pass

#    def build(self):
        # Hintergrundfarbe ist Weis
        #Window.clearcolor = (0.1, 0.3, 0.8, 1)
        #Window.clearcolor = (0.38, 0.35, 0.35, 1)
        #Window.clearcolor = [615959]
        # groesse des Fenters festlegen
        #Window.size = (800, 480)
        # Window.size = (2560,1440)
        #Window.size = (1920,1080)
        # ganzen Bildschirm
        #Window.fullscreen = True
#        canbusstatus.can0_check()
#        return Kivy_Beschreibung_laden

if __name__ == "__main__":
    programm().run()




