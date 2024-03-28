import pyautogui
import time

def press_key(key, number=None):
    if number:
        i = 0
        while(i < number):
            pyautogui.keyDown(key)
            time.sleep(0.1) 
            pyautogui.keyUp(key)
            i += 1
            print(i)
    else:
        pyautogui.keyDown(key)
        time.sleep(0.1)  
        pyautogui.keyUp(key)

    
def word_to_number(word):
    mots_numeriques = {
        'zéro': 0, 'un': 1, 'deux': 2, 'de': 2, 'trois': 3, 'quatre': 4,
        'cinq': 5, 'six': 6, 'si': 6, 'sept': 7,'cette': 7, 'huit': 8, 'neuf': 9,
        'dix': 10, 'dit': 10, 'onze': 11, 'douze': 12, 'treize': 13, 'quatorze': 14,
        'quinze': 15, 'seize': 16, 'dix-sept': 17, 'dix-huit': 18, 'dix-neuf': 19,
        'vingt': 20
    }

    if word in mots_numeriques:
        return mots_numeriques[word]
    else:
        return None

def recupNumber(chaine):
    mots = chaine.split()
    if len(mots) >= 3:
        return word_to_number(mots[2])
    if len(mots) >= 2:
        return word_to_number(mots[1])
    else:
        return 1

class Myinterpreter():
    def __init__(self):
        super().__init__()
        self.status = 1

    def interpret(self, data):
        data = data
        if(data):
            if data.find("oui") >= 0 or (data.find("oui") >= 0 and data.find("fois") >= 0):
                if data.find("fois") >= 0:
                    number = recupNumber(data)
                    press_key('l',number)
                    print("Bouton : 🅰️ * ",number)
                else:
                    press_key('l')
                    print("Bouton : 🅰️")
            if data.find("non") >= 0 or (data.find("non") >= 0 and data.find("fois") >= 0):
                if data.find("fois") >= 0:
                    number = recupNumber(data)
                    press_key('k',number)
                    print("Bouton : 🅱️ * ",number)
                else:
                    press_key('k')
                    print("Bouton : 🅱️")
            if data.find("en haut") >= 0 or (data.find("en haut") >= 0 and data.find("fois") >= 0):
                if data.find("fois") >= 0:
                    number = recupNumber(data)
                    press_key('up',number)
                    print("Bouton : ↑ * ",number)
                else:
                    press_key('up')
                    print("Bouton : ↑")
            if data.find("en bas") >= 0 or (data.find("en bas") >= 0 and data.find("fois") >= 0):
                if data.find("fois") >= 0:
                    number = recupNumber(data)
                    press_key('down',number)
                    print("Bouton : ↓ * ",number)
                else:
                    press_key('down')
                    print("Bouton : ↓")
            if data.find("a gauche") >= 0 or (data.find("a gauche") >= 0 and data.find("fois") >= 0):
                if data.find("fois") >= 0:
                    number = recupNumber(data)
                    press_key('left',number)
                    print("Bouton : ← * ",number)
                else:
                    press_key('left')
                    print("Bouton : ←")
            if data.find("a droite") >= 0 or (data.find("a droite") >= 0 and data.find("fois") >= 0):
                if data.find("fois") >= 0:
                    number = recupNumber(data)
                    press_key('right',number)
                    print("Bouton : → * ",number)
                else:
                    press_key('right')
                    print("Bouton : →")
            if data.find("menu") >= 0:
                press_key('return')
                print("Bouton : Start")
            if data.find("select") >= 0:
                press_key('backspace')
                print("Bouton : Select")
            if data.find("bouton air") >= 0:
                press_key('o')
                print("Bouton : R")
            if data.find("bouton elle") >= 0:
                press_key('i')
                print("Bouton : L")