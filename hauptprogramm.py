#!/usr/bin/python python
# -*- coding: utf-8 -*-

import subprocess
import os  # für den Dateibrowser
import time
from threading import Timer    # für den timer 2, 5 oder 10s
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition

from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup

from kivy.core.window import Window
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

    dateiname = ObjectProperty(False)


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

    def abspielen(self):
        '''
        Der Knopf Abspielen führt das Shell commando canplayer -l i -I aus, um die Daten
        auf dem Canbus zu senden.
        '''

        # wenn noch keine Datei ausgewählt wird eine Meldung ausgeben ansonsten starten
        if self.dateiname == False:
            root = self.parent
            # Label1 im Wiedergabebildschirm
            wiedergabebildschirm = root.ids.s2.ids.a1
            wiedergabebildschirm.text = "\n Bitte wählen Sie eine Datei aus!"

        else:
            #print(self.dateiname)
            p=subprocess.Popen("exec "+"canplayer -l i -I " + self.dateiname, shell=True)
            self.pid=p.pid


    def stop(self):
        subprocess.call("kill -9 " + str(self.pid), shell=True)
        pass

    pass
class Aufzeichnen(Screen):
    timer1 = ObjectProperty(False)

    global messung_gestartet
    messung_gestartet = False

    def dateiname_erstellen(self):
        #print(time.strftime("%d.%m.%Y %H:%M:%S"))
        dateiname_zeit=time.strftime("%Y_%d_%m__%H_%M_%S")+ ".log"
        return dateiname_zeit

    def start_messung(self):

        global messung_gestartet
        if messung_gestartet == False:
            self.aufzeichnen()
            messung_gestartet=True

    def aufzeichnen(self):

        # root ist Bildschirmverwalter
        root = self.parent
        # Label2 a2 im Aufzeichnungsbildschirm Anzeige wird gelöscht
        aufzeichnungsbildschirm = root.ids.s3.ids.a2
        aufzeichnungsbildschirm.text = ""
        # Label3 a3 im Aufzeichnungsbildschirm Anzeige wird gelöscht
        aufzeichnungsbildschirm = root.ids.s3.ids.a3
        aufzeichnungsbildschirm.text = ""
        # Label1 im Aufzeichnungsbildschirm
        aufzeichnungsbildschirm = root.ids.s3.ids.a1
        global can0_exist
        if can0_exist == True:
            global messdauer, aufzeichnung
            dateiname = self.dateiname_erstellen()
            # Aufzeichnung starten

            befehl="exec candump -L can0 >./Logs/"+ str(dateiname)
            aufzeichnung=subprocess.Popen(befehl , shell=True)
            self.aufzeichnungsPID=aufzeichnung.pid
            #print("PID: \t",aufzeichnung.pid)

            # Start des Timers
            fenster_record=self
            self.timer1=RepeatedTimer(1, int(messdauer), fenster_record,dateiname)


        else:
            aufzeichnungsbildschirm.text = "\n Es existiert KEINE Cankarte!" \
                                           "\n\n Eine Aufzeichnung ist nicht möglich."
            pass
        pass

    def stop(self):
        # Status der Messung wird gesetzt
        global messung_gestartet
        messung_gestartet = False

        if not self.timer1 == False:
            self.timer1.stop()
            #print(self.aufzeichnungsPID)
            subprocess.call("kill -9 " + str(self.aufzeichnungsPID), shell=True)
            pass
        else:
            global aufzeichnung
            subprocess.call("kill -9 " + str(aufzeichnung.pid), shell=True)
            pass
    pass

class RepeatedTimer(object):

    def __init__(self, interval, messdauer, fenster_record, dateiname, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()
        self.counter    = messdauer
        self.fenster    =fenster_record
        self.dateiname  =dateiname
        # root ist Bildschirmverwalter
        root = self.fenster.parent
        # Label1 im Bildschim Aufzeichnung
        Aufzeichnungsbildschirm = root.ids.s3.ids.a1
        Aufzeichnungsbildschirm.text = "\n Die Messung wurde gestartet!"

    def _run(self):
        self.is_running = False
        self.start()
        self.counter -=1
        self.aktuelle_messdauer()
        if self.counter== 0:
            # timer stop
            self.stop()
            #Aufzeichnung stoppen
            Aufzeichnen().stop()
            print ("Fertig!")

    def start(self):

        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True


    def stop(self):
        self._timer.cancel()
        self.is_running = False
        # root ist Bildschirmverwalter
        root = self.fenster.parent
        # Label1 a1 im Bildschim Aufzeichnung
        aufzeichnungsbildschirm = root.ids.s3.ids.a1
        aufzeichnungsbildschirm.text = "\n Die Messung beendet! "
        # Label3 a3 im Bildschim Aufzeichnung
        aufzeichnungsbildschirm = root.ids.s3.ids.a3
        aufzeichnungsbildschirm.text = "\n Messung wurde gespeicht unter:" \
                                       "\n    "  + str(self.dateiname)
        # Status der Messung wird gesetzt
        global messung_gestartet
        messung_gestartet = False


    def aktuelle_messdauer(self):
        '''aus gabe der aktuellen Messdauer im Fenster Aufzeichnung'''
        # root ist Bildschirmverwalter
        root = self.fenster.parent
        ## Label1 im Aufzeichnungsbildschirm
        aufzeichnungsbildschirm = root.ids.s3.ids.a2
        aufzeichnungsbildschirm.text = "\n  verbleibende Messzeit: " \
                                       "" + str(self.counter) + "s"

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

        # Messdauer
        global messdauer
        messdauer = self.config.get('Aufzeichnung', 'dauer')

        # Hintergrundfarbe ist Weis
        #Window.clearcolor = (0.1, 0.3, 0.8, 1)
        #Window.clearcolor = (0.38, 0.35, 0.35, 1)
        #Window.clearcolor = [615959]
        # groesse des Fenters festlegen
        Window.size = (800, 480)
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

    def pfad_wiedergabe(self):
        '''
        ermittelt den Pfad der unter Einstellungen für die Wiedergabe
        ausgewählt wurde
        '''
        pfad = self.config.get('Wiedergabe', 'path')
        return pfad

if __name__ == "__main__":
    programm().run()




