#!/usr/bin/env python3


import string
from tokenize import String
from xml.dom.minidom import ReadOnlySequentialNamedNodeMap
import torch
import cv2
import numpy as np

#librerias necesarias
import rospy # Libreria de ROS para Python 
from sensor_msgs.msg import Image # Imagen definida como tipo de mensaje
from cv_bridge import CvBridge # Paquete para convertir entre ROS y OpenCV las imagenes
import cv2 # Libreria OpenCV
from pathlib import Path
from std_msgs.msg import String      


model = torch.hub.load('/home/santiago/Descargas/K3LSO/Reconocimiento_video/', 'custom',
                       path = '/home/santiago/Descargas/K3LSO/Reconocimiento_video/yolov5s.pt',source='local') #modelo offline

pub = rospy.Publisher('objects', String,queue_size=10)


def listToString(s):
   
    # initialize an empty string
    str1 = " "
   
    # return string 
    return (str1.join(s))

def callback(data):
 
  # convertir entre imágenes ROS y OpenCV
  br = CvBridge()
 
  # Output debugging information to the terminal
  #rospy.loginfo("receiving video frame")
 
# Convertir mensaje de imagen ROS a imagen OpenCV
  global datos,info
  current_frame = br.imgmsg_to_cv2(data)
  detect = model(current_frame)
  info = detect.pandas().xyxy[0]
  unique_arr = info["name"].unique()
  #print(unique_arr)
  datos = listToString(unique_arr)
  # for row in info.name:
  #       print(row , end = "\n")
  #       datos = row


  #for row in info.name:  
    #print(row , end = "\n")
  # Display image
  cv2.imshow('Detector de objetos', np.squeeze(detect.render()))

  cv2.waitKey(1)

def callback_2(message):
  global x, datos, dato_anterior
  dato_actual = datos
  if dato_anterior == dato_actual:
    pass
  else:
    pub.publish(datos)
  dato_anterior = dato_actual
  #print("mensaje publicado")



def receive_message():
  global dato_anterior
  dato_anterior = ""
  # Le dice a Rospy el nombre del nodo.
  # anonymous = True se asegura de que el nodo tenga un nombre único. Aleatorio
  # números se agregan al final del nombre.
  rospy.init_node('video_sub_py', anonymous=True)
  
  # Nodo se suscribe a el tópico video_frames
  rospy.Subscriber('video_frames', Image, callback)
  timer = rospy.Timer(rospy.Duration(0.5), callback_2)

  print("si entra")
 # spin() simplemente permite que python exista hasta que se detenga este nodo
  rospy.spin()
  timer.shutdown()
  # Cierre la transmisión de video cuando haya terminado
  cv2.destroyAllWindows()
  
if __name__ == '__main__':
  receive_message()