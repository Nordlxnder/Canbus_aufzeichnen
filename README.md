# Canbus_aufzeichnen
Funktion:
 
	Programm um CANBUS Botschaften zu senden oder aufzuzeichnen
	
	Aufzeichnungszeit (2s,5s und 10s) auswähltbar
	
	Die aufgezeichneten Daten werden im Ordner Logs als Datum_Zeit.log 
	gespeichert.	

Anwendung: 

	Raspberry PI 3 oder Banana Pi mit Canbusschnittstelle
        Die Bedienung ist über ein Touchdisplay (800x 480) möglich

	Die Bilder für die Knöpfe sind für eine Auflösung von 800x480 
	optimiert

Voraussetzung:
	
	can0 Schnittstelle sollte vorhanden sein 
	-----------------------------------------------

	Der Benutzer sollte den Befehl "ip" ohne Rootrechte ausführen können
	Dies kann man mit dem Eintrag in der /etc/sudoers erreichen
	##
	## User privilege specification
	##
	root ALL=(ALL) ALL
	username ALL=(ALL) ALL
	usersname ALL=(ALL) NOPASSWD: /sbin/ip
	


Software:

	Archlinux
	Python 3
	Kivy 
	sudo

Hardware:

	Raspberry Pi3 mit Can-Erweiterung
	Banana Pi mit Can-Erweiterung
	Touch Display 800x480 (andere sollten auch möglich sein;)

