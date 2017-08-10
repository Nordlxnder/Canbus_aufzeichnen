import json

settings_can = json.dumps([
    {'type': 'options',
     'title': 'Baudrate',
     'desc': 'Auswahl der Busgeschwindigkeit',
     'section': 'CANBUS',
     'key': 'baudrate',
     'options': ['250 kHz', '500 kHz', '1000 kHz']},
    ])
settings_rekord = json.dumps([
    {'type': 'path',
     'title': 'Verzeichnis',
     'desc': 'Pfad für Logdateien',
     'section': 'Aufzeichnung',
     'key': 'path'},
    {'type': 'options',
     'title': 'Aufzeichnungsdauer',
     'desc': 'Dauer der Aufzeichnung in Sekunden',
     'section': 'Aufzeichnung',
     'key': 'dauer',
     'options': ['2', '5', '10']},
    ])
settings_play = json.dumps([
    {'type': 'path',
     'title': 'Verzeichnis',
     'desc': 'Pfad für die Datei, die Wiedergeben werden soll',
     'section': 'Wiedergabe',
     'key': 'path'},
    ])