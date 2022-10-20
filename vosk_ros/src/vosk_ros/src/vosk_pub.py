#!/usr/bin/env python3                         
# encoding: utf-8

#Linea 1 - “Shebang”,le indicamos a la máquina con qué programa lo vamos a ejecutar.
#Linea 2 - Python 3 - asume que solo se utiliza ASCII en el código fuente
#para usar utf-8 hay que indicarlo al principio de nuestro script encoding: utf-8

#librerias vosk
from vosk import Model, KaldiRecognizer
import pyaudio
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
#
import os
import rospy                                                #Importamos ropsy (interface de python-ROS) 
from std_msgs.msg import String                             #Importamos tipo de mensaje String


#modelo vosk
model = Model(r"/home/santiago/Descargas/K3LSO/vosk-model-es-0.42")
recognizer = KaldiRecognizer(model,16000)
mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16,channels = 1,rate = 16000,input = True,frames_per_buffer = 8192)
stream.start_stream()

def nodo():                                                 #Definimos una función nodo                                   
    
    rospy.init_node('vosk_pub')                       #Inicializamos nuestro nodo y le asignamos un nombre = nodo_publisher
    
    pub = rospy.Publisher('deteccion', String, queue_size=10) #Definimos nuestro topico con nombre example y tipo de mensaje String
                                                            #con un límite de 10 mensajes en cola 
    rate = rospy.Rate(10)                                   #Crea un objeto Rate a 10hz (loop 10 times per second)
    
    while not rospy.is_shutdown(): 
        instruccion = " "
        data = stream.read(4896)                         #Bucle While - hasta pulsar Ctrl-C       
        if recognizer.AcceptWaveform(data):
            text = recognizer.Result()
            #print(text)
            #instruccion = word_tokenize(text[14:-3])
            instruccion = text[14:-3]
            #print(instruccion)

        #mensaje = "Nodo Publisher"                          #Declaramos una variable mensaje y asignamos una cadena de caracteres
        
        #rospy.loginfo(instruccion)                              #Imprime en pantalla mensajes logs de tipo Info
        if(instruccion== ""):
            pass
        else:
            pub.publish(instruccion)                                #Publicamos un mensaje de tipo String en nuestro tópico example 
        
        rate.sleep()                          

if __name__ == '__main__':                                  #Llamamos a la función principal main
    try:
        nodo()                                              # Lamamos a la función nodo
    except rospy.ROSInterruptException:                     # Check si hay una excepción  Ctrl-C para terminar la ejecución del nodo
        pass