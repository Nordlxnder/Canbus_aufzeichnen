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

from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup

#from kivy.core.window import Window
from settingscanbus import settings_can , settings_rekord ,settings_play
#from kivy.uix.settings import SettingsWithSidebar

import canbusstatus

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class Bildschirmverwalter(ScreenManager):   pass
class Hauptbildschirm(Screen):  pass
class Wiedergabe(Screen):
    ''' Fenster Wiedergabe enthält die Bedienelemente und Funktionen, die für eine Wiedergabe benötigt werden'''

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        inhalt = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Datei auswählen und laden", content=inhalt,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        global can0_exist
        if not filename:
            # root ist Bildschirmverwalter
            root = self.parent
            # Label1 im Wiedergabebildschirm
            wiedergabebildschirm = root.ids.s2.ids.a1
            wiedergabebildschirm.text = "\n Es wurde keine Datei ausgewählt!"
        else:
            self.dateiname = filename[0]
            # filename enthält den Pfad und den Dateinamen
            # Das Element wird aufgeteilt, separator ist /
            # In der neuen Liste ist das letzte Element [-1] der Dateiname
            dateiname = str(filename[0].split("/")[-1])
            # root ist Bildschirmverwalter
            root = self.parent
            # Label1 im Wiedergabebildschirm
            wiedergabebildschirm = root.ids.s2.ids.a1
            if can0_exist == True:
                wiedergabebildschirm.text = "\n Es wurde die Datei " + dateiname + " ausgewählt!"
            else:
                wiedergabebildschirm.text = "\n Es wurde die Datei " + dateiname \
                                            + " ausgewählt! \n\n Es existiert aber KEINE Cankarte! ;))"
            pass

        self.dismiss_popup()



    pass
class Aufzeichnen(Screen): pass

# Alle im der KV Datei verwendeten Klassen müssen vor dem Laden definiert sein
# Die Klassen werden dann beim Laden aufgerufen
#Kivy_Beschreibung_laden = Builder.load_file('canbusanzeige.kv')

class programm(App):
    '''
    Funktionen:

      0 Titel des Fensters festlegen

      1  Prüfung beim Start ob eine CAN Karte vorhanden ist

      2 Objekt root der Variable Bildschirmverwalter zuordnen,
        damit die Fenster und widgets von Python angesprochen werden können

      3 Konfiguration Datei für die Einstellungen erstellen, auslesen und
        aktivieren bei einer Veränderung der Parameter

      4 Pfad für die Wiedergabe ermitteln und der Variable pfad zuordnen


    '''
    # ob can0 existiert True oder False
    # self.can0_exist=can0_exist
    title = 'Canbus Rekorder'
    #    icon = 'canbus2.png'


    pass

    def build(self):

        Bildschirmverwalter=self.root

        # Überprüfung und Anzeige auf den Hauptbildschirm
        # ob eine Cankarte vorhaden ist
        global can0_exist
        label_hauptbildschirm = Bildschirmverwalter.ids.s1.ids.l1
        can0_exist=canbusstatus.can0_check(label_hauptbildschirm)


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

    def build_config(self, config):
        # Programmpfad auslesen
        pfad = os.getcwd() + "/Logs"
        # setzt die Standardwerte für die Einstellungen
        config.setdefaults('CANBUS', {
            'baudrate': '500 kHz'})

        config.setdefaults('Aufzeichnung', {
            'path': pfad,
            'dauer': '5'})

        config.setdefaults('Wiedergabe', {
            'path': pfad})

    def build_settings(self, settings):
        '''
        Das Konfigurationfeld wird hinzugefügt
        '''
        settings.add_json_panel('CANBUS Einstellungen',
                                self.config,
                                data=settings_can)
        settings.add_json_panel('Aufzeichnung',
                                self.config,
                                data=settings_rekord)
        settings.add_json_panel('Wiedergabe',
                                self.config,
                                data=settings_play)

    def on_config_change(self, config, section, key, value):
        # print (config, section, key, value)
        '''
        Bei einer Änderung der Einstellungen werden diese in die INI Datei
        geschrieben und aktiviert
        '''
        # Messdauer nach Änderung neu setzen
        global messdauer, can0_exist
        messdauer = self.config.get('Aufzeichnung', 'dauer')

        if key == "path":
            # Überprüfung ob der Pfad richtig gewählt wurde
            try:
                pfad = "'" + value + "'"
                subprocess.check_call('[ -d ' + pfad + '  ]', shell=True)
            except:
                # Anpassung des Pfads , der Pfad wird bis auf das letzte / gekürzt
                liste = [pos for pos, char in enumerate(value) if char == '/']
                neuer_pfad = value[0:liste[-1]]
                # Neuer Pfad wird gesetzt und in die ini Datei (programm.ini) geschrieben
                config.set('CANBUS', 'path', neuer_pfad)
                config.write()


        if can0_exist == True:
            baudrate_soll = self.config.get('CANBUS', 'baudrate')
            canbusstatus.can_set_baudrate(baudrate_soll)
        # Anzeige aktualisieren im Hauptfenster
            status = canbusstatus.can_read_baudrate()
            Bildschirmverwalter=self.root
            label_hauptbildschirm = Bildschirmverwalter.ids.s1.ids.l1
            label_hauptbildschirm.text="\nDie CAN Karte ist " + status[1] + "\nBaudrate: " + status[0]
            # root = objekt Bildverwalter oberste Ebene
        #    root = self.root
        #    # Anzeige1 --> Label1 im Hauptbildschirm
        #    Hauptbildschirm = root.ids.s1.ids.a1.ids.w1
        #    Hauptbildschirm.text = "\nDie CAN Karte ist " + status[1] + "\nBaudrate: " + status[0]

    def pfad_wiedergabe(self):
        '''
        ermittelt den Pfad der unter Einstellungen für die Wiedergabe
        ausgewählt wurde
        '''
        pfad = self.config.get('Wiedergabe', 'path')
        return pfad

if __name__ == "__main__":
    programm().run()




