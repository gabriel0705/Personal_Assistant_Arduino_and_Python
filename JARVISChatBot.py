import serial 
import threading
import time
import speech_recognition as sr
import pyttsx3 

#chatbot lib
from chatterbot.trainers import ListTrainer 

from chatterbot import ChatBot


JARVISbot = ChatBot("JARVIS")

 #texto inicial, com as conversas o bot vai ficando mais inteligente
conversa1 = ['hello jarvis','hello sir','how you doing ?', 'im great,how about you?','jarvis','im here sir','yes sir']
conversa2 = ['whats up Jarvis?','hey Gabriel','are you feeling good ?','cant be better! how can I help you ?']
conversa3 = ['i am fine', 'thats great','thank you','your welcome sir','thanks','my pleasure','how are you','im great,thanks for asking']
conversa4 = ['jarvis what is my name?', 'you are gabriel, my creator', 'turn on video game', 'unfortunately i cant do that because im not programmed to this function yet']
conversa5 = ['can you tell me a joke?', 'im not great with jokes, but here it goes. Why six was afraid of seven?', 'why?', 'because seven ate nine']
conversa6 = ['jarvis who is my grandfather ?','your grandfather is Almeer','jarvis say hello','hey everyone']
conversa7 = ['who are you?','i am jarvis, a personal assistent created by Gabriel de Lemos']
conversa8 = ['im fine','cool','good morning jarvis','good morning sir','good evening jarvis','good evening sir','nice to meet you','nice to meet you too']
conversa9 = ['how is the weather today','today is a great day to work sir, for more especific details access the weather forecast','jarvis say hi to my teacher','hello Gabriels teacher, how you doing?']
conversa10 = ['jarvis what do you think about artificial intelligence','well,thats a great subjact,artificial intelligence is intelligence demonstrated by machines,the capacity of showing cognitive functions that humans associate with the human mind, such as learning and problem solving']
conversa11 = ['how do you know about this','every thing is on the internet sir','what do you thing about education','Education gives us an understanding of the world around us and offers us an opportunity to use that knowledge wisely,Irrespective of race, creed, and gender, education makes it possible for people to stand out as equal with all the other persons from different walks of life']
conversa12 = ['what is the theory of relativity','Einsteins theory of special relativity says that time slows down or speeds up depending on how fast you move relative to something else,Approaching the speed of light, a person inside a spaceship would age much slower than his twin at home, Also, under Einsteins theory of general relativity, gravity can bend time']
conversa13 = ['who was Albert Einstein','Albert Einstein was a German-born theoretical physicist who developed the theory of relativity, one of the two pillars of modern physics,alongside quantum mechanics']
conversa14 = ['jarvis say hello to in metrics', 'hello people from inmetrics, my name is Jarvis a personal assistant created by Gabriel de Lemos', 'good jarvis and what do you have to say to them', 'i hope gabriel made a great presentation, after all i cant speak badly of him because he programmed me to say only great things']

treinar = ListTrainer(JARVISbot)
treinar.train(conversa1)
treinar.train(conversa2)
treinar.train(conversa3)
treinar.train(conversa4)
treinar.train(conversa5)
treinar.train(conversa6) 
treinar.train(conversa7)
treinar.train(conversa8)
treinar.train(conversa9) 
treinar.train(conversa10)
treinar.train(conversa11)
treinar.train(conversa12)
treinar.train(conversa13)
treinar.train(conversa14)



engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('rate', 170) 
contar = 0;
for vozes in voices: # lista as vozes disponiveis
    print(contar, vozes.name)
    contar+=1

voz = 0
engine.setProperty('voice', voices[voz].id)


r = sr.Recognizer()

mic = sr.Microphone(0) 

conectado = False
porta = 'COM3' 
velocidadeBaud = 115200

mensagensRecebidas = 1;
desligarArduinoThread = False

falarTexto = False;
textoRecebido = ""
textoFalado = ""

arduinoFuncionando = True

try:
    SerialArduino = serial.Serial(porta,velocidadeBaud, timeout = 0.2)
except:
    print("Verify serial port or restart JARVIS")
    arduinoFuncionando = False

def handle_data(data):
    global engine, falarTexto, textoRecebido
    print("I Say " + ": " + data)
    
    textoRecebido = data
    falarTexto = True

def read_from_port(ser):
    global conectado, desligarArduinoThread
    
    while not conectado:
        conectado = True

        while True:
           reading = ser.readline().decode()
           if reading != "":
               handle_data(reading)
           if desligarArduinoThread:
               print("Turning JARVIS off ...")
               break
           
if arduinoFuncionando:
    try:
        lerSerialThread = threading.Thread(target=read_from_port, args=(SerialArduino,))
        lerSerialThread.start()
    except:
        print("Verify serial port or restart JARVIS")
        arduinoFuncionando = False
    print("Preparing JARVIS ...")
    time.sleep(2)
    print("JARVIS is ready")
else:
    time.sleep(2)
    print("JARVIS not connected")

while (True):
    if falarTexto:
        if textoRecebido != "":
            engine.say(textoRecebido)
            engine.runAndWait()
            textoRecebido = ""
        elif textoFalado != "":
            resposta = JARVISbot.get_response(textoFalado)
            engine.say(resposta)
            engine.runAndWait()
            textoFalado = ""
        
       
        
        falarTexto = False
        
    try:
        with mic as fonte:
            r.adjust_for_ambient_noise(fonte)
            print("Say something:")
            audio = r.listen(fonte)
            print("Recognizing ...")
        try:
            text = r.recognize_google(audio).lower()
            print("You said: {}".format(text))
            if text == "turn off the lights" or text == "turn on the lights":
                try:
                    pass
                    
                except:
                    print("without socket")
            if arduinoFuncionando:
                SerialArduino.write((text + '\n').encode())
            
            if text != "":
                textoFalado = text
                falarTexto = True
            
            print("Data Sent")
            if(text == "deactivate"):
                print("Deactivating...")
                
                desativando = "Jarvis offline, goodbye mister Gabriel."
                
                engine.say(desativando)
                engine.runAndWait()
                
                
                engine.stop()
                desligarArduinoThread = True
                if arduinoFuncionando:
                    SerialArduino.close()
                    lerSerialThread.join()
                break
        except:
            print("I dont understend you\n")
            
            engine.runAndWait()
        
        time.sleep(0.5) # aguarda resposta do arduino
    except (KeyboardInterrupt, SystemExit):
        print("Apertou Ctrl+C")
        engine.stop()
        desligarArduinoThread = True
        if arduinoFuncionando:
            SerialArduino.close()
            lerSerialThread.join()
        break
