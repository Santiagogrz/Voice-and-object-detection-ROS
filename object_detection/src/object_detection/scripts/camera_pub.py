#!/usr/bin/env python3

 
# Importar las bibliotecas necesarias
import rospy # Libreria de ROS para Python 
from sensor_msgs.msg import Image # Imagen definida como tipo de mensaje
from cv_bridge import CvBridge # Paquete para convertir entre ROS y OpenCV las imagenes
import cv2 # Libreria OpenCV
#from std_msgs.msg import MultiArrayDimension  

def publish_message():
  # El nodo está publicando en el tópico video_frames usando 
  # El tipo de mensaje Imagen
  pub = rospy.Publisher('video_frames', Image, queue_size=10)
     
  # Le dice a Rospy el nombre del nodo.
  # anonymous = True se asegura de que el nodo tenga un nombre único. Aleatorio
  # números se agregan al final del nombre.
  rospy.init_node('video_pub_py', anonymous=True)
     
  # Pasa por el bucle 15 veces por segundo, envia 15 frames
  rate = rospy.Rate(15) # 15hz
     
  # Crear un objeto VideoCapture
  # El argumento '0' obtiene el valor por defecto de la webcam.
  
  cap = cv2.VideoCapture(0)

  # convertir entre imágenes ROS y OpenCV
  br = CvBridge()
  
  # Mientras ROS esta ejecutando:
  while not rospy.is_shutdown():
     
      # Obtener frame por frame
      # Este método también devuelve Verdadero/Falso cuadro de video.
      ret, frame = cap.read()
         
      if ret == True:
        # Print debugging information to the terminal
        #rospy.loginfo('publishing video frame')
             
        # Publicar la imagen.
        # El método 'cv2_to_imgmsg' convierte un OpenCV imagen a un mensaje de imagen ROS
        pub.publish(br.cv2_to_imgmsg(frame))
             
      # retardo suficiente para mantener el ritmo deseado
      rate.sleep()
         
if __name__ == '__main__':
  try:
    publish_message()
  except rospy.ROSInterruptException:
    pass