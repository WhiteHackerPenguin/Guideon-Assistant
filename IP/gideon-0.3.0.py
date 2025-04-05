'''
    Description: 
    Author: Julian Principe, AVM, Blackbox
    Version: 0.3.0
'''
import AVMSpeechMath as sm
import AVMYT as yt
import speech_recognition as sr
import pyttsx3
import pywhatkit
import json
from datetime import datetime, date, timedelta
import wikipedia
import pyjokes
import os
from time import time

start_time = time()
engine = pyttsx3.init()

# name of the virtual assistant
name = 'gideon'
name_1 = 'didion'
name_2 = 'videos'
name_3 = 'bideon'
attemts = 0

# keys
with open('src/keys.json') as json_file:
    keys = json.load(json_file)

# colors
green_color = "\033[1;32;40m"
red_color = "\033[1;31;40m"
normal_color = "\033[0;37;40m"

# get voices and set the first of them
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# editing default configuration
engine.setProperty('rate', 178)
engine.setProperty('volume', 0.7)

day_es = [line.rstrip('\n') for line in open('src/day/day_es.txt')]
day_en = [line.rstrip('\n') for line in open('src/day/day_en.txt')]

def iterateDays(now):
    for i in range(len(day_en)):
        if day_en[i] in now:
            now = now.replace(day_en[i], day_es[i])
    return now

def getDay():
    now = date.today().strftime("%A, %d de %B del %Y").lower()
    return iterateDays(now)

def getDaysAgo(rec):
    value =""
    if 'ayer' in rec:
        days = 1
        value = 'ayer'
    elif 'antier' in rec:
        days = 2
        value = 'antier'
    else:
        rec = rec.replace(",","")
        rec = rec.split()
        days = 0

        for i in range(len(rec)):
            try:
                days = float(rec[i])
                break
            except:
                pass
    
    if days != 0:
        try:
            now = date.today() - timedelta(days=days)
            now = now.strftime("%A, %d de %B del %Y").lower()

            if value != "":
                return f"{value} fue {iterateDays(now)}"
            else:
                return f"Hace {days} días fue {iterateDays(now)}"
        except:
            return "Aún no existíamos"
    else:
        return "No entendí"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_audio():
    r = sr.Recognizer()
    status = False

    with sr.Microphone() as source:
        print(f"{green_color}({attemts}) Escuchando...{normal_color}")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
        rec = ""

        try:
            rec = r.recognize_google(audio, language='es-ES').lower()
            
            if name or name_1 or name_2 or name_3 in rec:
                rec = rec.replace(f"{name} ", "").replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
                status = True
            else:
                print(f"Vuelve a intentarlo, no reconozco: {rec}")
        except:
            pass
    return {'text':rec, 'status':status}

while True:
    rec_json = get_audio()

    rec = rec_json['text']
    status = rec_json['status']

    if status:
        if 'estas ahi' in rec:
            speak('Si me necesitas para algo, ten por seguro que siempre estoy aquí.')

        elif 'reproduce' in rec:
                music = rec.replace('reproduce', '')
                speak(f'Reproduciendo {music}')
                #yt.play(music)
                pywhatkit.playonyt(music)
        
        elif 'cuantos suscriptores tiene' in rec:
            name_subs = rec.replace('cuantos suscriptores tiene', '')
            
            speak("Procesando...")
            while True:
                try:
                    channel = yt.getChannelInfo(name_subs)
                    speak(channel["name"] + " tiene " + channel["subs"])
                    break
                except:
                    speak("Volviendo a intentar...")
                    continue

        elif 'que' in rec:
            if 'hora' in rec:
                hora = datetime.now().strftime('%I:%M %p')
                speak(f"Son las {hora}")

            elif 'dia' in rec:
                if 'fue' in rec:
                    speak(f"{getDaysAgo(rec)}")
                else:
                    speak(f"Hoy es {getDay()}")
                    
        elif 'qué' in rec:
            if 'hora' in rec:
                hora = datetime.now().strftime('%I:%M %p')
                speak(f"Son las {hora}")
                
            elif 'día' in rec:
                if 'fué' in rec:
                    speak(f"{getDaysAgo(rec)}")
                else:
                    speak(f"Hoy es {getDay()}")

        elif 'busca' in rec:
            order = rec.replace('busca', '')
            wikipedia.set_lang("es")
            info = wikipedia.summary(order, 1)
            speak(info)

        elif 'un chiste' in rec:
            chiste = pyjokes.get_joke("es")
            speak("okey, aí va uno." + chiste)
            
        elif 'otro chiste' in rec:
            chiste = pyjokes.get_joke("es")
            speak("okey, aí va otro.a ver si este te gusta mas." + chiste)

        elif 'cuanto es' in rec:
            speak(sm.getResult(rec))

        elif 'todo bien' in rec:
            speak("Por Supuesto.¿Quieres que te ayude con algo?")

        elif 'si' in rec:
            speak("Adelante. Dime en que te puedo ayudar...")
            
        elif 'sí' in rec:
            speak("Adelante. Dime en que te puedo ayudar...")
            
        elif 'buenos dias' in rec:
            speak("Buenos Días. Espero que tengas un muy lindo día")
            
        elif 'buenas tardes' in rec:
            speak("Buenas tardes. Necesitas algo?")

        elif 'gracias' in rec:
            speak("De nada. Estoy aqí para ayudarte.¿Necesitas algo?")
        
        elif 'muchas gracias' in rec:
            speak("De nada, para eso estoy. Necesitas algo mas?")

        elif 'mierda' in rec:
            speak("Bueno, no es necesario insultar.¿necesitas otra cosa?")

        elif "bueno" in rec:
            speak("Tengo más.¿Quieres otro?")

        elif 'espectacular' in rec:
            speak("Gracias. ¿Algo mas?")
        
        elif 'abrir notepad' in rec:
          nombre_bloque_notas = rec.split()[-1] + ".txt"
          ruta_bloque_notas = f"RUTA_A_TU_BLOQUE_DE_NOTAS/{nombre_bloque_notas}"  # Replace for the correct path
    
          if os.path.exists(ruta_bloque_notas):
            os.startfile(ruta_bloque_notas)
            speak(f"Abriendo el Bloc de notas {nombre_bloque_notas}")
          else:
            speak(f"No se encontró un Bloc de notas con el nombre {nombre_bloque_notas}")
            
        elif 'buenas noches' in rec:
            speak("Buenas noches.Que duermas bien")
            break
        
        elif 'descansa' in rec:
            speak("Saliendo...")
            break

        else:
            print(f"Vuelve a intentarlo, no reconozco: {rec}")
        
        attemts = 0
    else:
        attemts += 1

print(f"{red_color} ASISTENTE FINALIZADO CON UNA DURACIÓN DE: { int(time() - start_time) } SEGUNDOS {normal_color}")
