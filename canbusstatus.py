
import subprocess

def can0_check():
    ''' prüft ob can0 auf dem PC existiert'''

    try:
        ausgabe = subprocess.check_output('ip -details link show vcan0', shell=True)
        print("Eine Cankarte ist vorhanden")
        return True
    except:
        print("Es ist keine Cankarte vorhanden")
        return False