#!/usr/bin/env python3                         
# encoding: utf-8

#Linea 1 - “Shebang”,le indicamos a la máquina con qué programa lo vamos a ejecutar.
#Linea 2 - Python 3 - asume que solo se utiliza ASCII en el código fuente
#para usar utf-8 hay que indicarlo al principio de nuestro script encoding: utf-8

from email.mime import image
from queue import Empty
from re import X
from unicodedata import numeric
import nltk
import rospy                                                #Importamos ropsy (interface de python-ROS) 
from std_msgs.msg import String                             #Importamos tipo de mensaje String
from nltk.tokenize import word_tokenize
from sensor_msgs.msg import Image 
import pyttsx3
from datetime import datetime
import playsound
name = "kelso"
pub = rospy.Publisher('actions', String, queue_size=10) #Definimos nuestro topico con nombre example y tipo de mensaje String


def speak(data):
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)
    engine.say(data)
    engine.runAndWait() 

def saludo():
    speak("Hello, how are you")

def hora():
    now = datetime.now()
    speak(str(now.hour))    
    speak(str(now.minute))

def reproducir_sonido():
    playsound.playsound('/home/santiago/Descargas/ladrido.mp3')

def nombre():
    speak("Hello, my name is kelso")

def accion(action):
    speak("Executing action")
    pub.publish(action)                                

    #se envian los caracteres para buscar en los diccionarios ya establecidos

def callback(mensaje):
    
    if len(mensaje.data) <= 1:
        pass
        
    else:
        rospy.loginfo("Mensaje recibido %s", mensaje.data)
        if "kelso" in mensaje.data:
            print("si esta mi nombre")
            if 'hola' in mensaje.data:
                saludo()
            elif 'hora' in mensaje.data:
                hora()
            elif 'adelante' in mensaje.data:
                accion('i')
            elif 'derecha' in mensaje.data:
                accion("l")
            elif 'izquierda' in mensaje.data:
                accion("j")
            elif 'atrás' in mensaje.data:
                accion(",")
            elif 'frente' in mensaje.data:
                nombrar_objetos()
            elif 'vuelta' in mensaje.data:
                accion("m")
            elif 'ladra' in mensaje.data:
                reproducir_sonido()

        elif 'nombre' in mensaje.data:
            nombre()
        else:
            print("No dijiste mi nombre")

def nombrar_objetos():
    
    if datos_recibidos[0] == "":
        speak("I am not seeing anything")
    else:
        speak(datos_recibidos)

def callback2(mensaje2):
    global datos_recibidos
    datos_recibidos = convert(mensaje2.data)
    print("objetos detectados:",datos_recibidos)


def convert(string):
    li = list(string.split(" "))
    return li

def nodo():                                                 #Definimos una función nodo                                   

    rospy.init_node('vosk_pub')                      #Inicializamos nuestro nodo y le asignamos un nombre = transmisor    
        
    rospy.Subscriber("deteccion", String, callback)         #Realizamos la subscripción al tópico example con tipo de mensaje String     
    
    rospy.Subscriber('objects',String,callback2)
    
    rospy.spin()                                            #Mantiene corriendo el script hasta que se detiene la ejecución con Crtl+C

if __name__ == '__main__':                                  #Llamamos a la función principal main
    try:
        nodo()                                              # Lamamos a la función nodo
    except rospy.ROSInterruptException:                     # Check si hay una excepción  Ctrl-C para terminar la ejecución del nodo
        pass