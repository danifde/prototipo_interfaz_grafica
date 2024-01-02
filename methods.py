import dlib
import cv2
import os
import face_recognition
import struct
import numpy as np
from database import DataBase
from querys import Querys

class Register:

    # Creamos la instancias para establecer la conexión a la base de datos
    # Creamos la instancia para ejecutar la sentencia SQL requerida
    def __init__(self):
        self.querys = Querys()
        self.database = DataBase()

        # Establecemos la dirección relativa para el almacenamiento de las imagenes
        self.path_dir = "./imgs"
        self.name_dir = "data"


    # Método que crea un registro de un usuario en la base de datos
    def create_register_user(self, document_number, names, last_names, gender):

        # Guardamos la imagen del rostro en un directorio, de la persona que registramos en la base de datos
        path_img = os.path.join(self.path_dir, self.name_dir)
        if not os.path.exists(path_img):
            os.makedirs(path_img) 

        # Iniciamos la captura de frames en tiempo real
        cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

        # Determinamos si se encuentra una cara en el frame capturado
        detector = dlib.get_frontal_face_detector()

        # Creamos una variable, la cual tendrá la función de determinar la cantidad de frames a capturar
        cont = 0

        while True:
            ret, frame = cap.read()
            if ret == False:
                break

            # Convertimos la imagen a escala de grises
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Comprobamos que en la imagen se encuentre un rostro
            faces = detector(gray)
            if faces is not None:

                # Iteramos sobre el rostro para determinar sus dimensiones y coordenadas
                for face in faces:
                    x, y, w, h = face.left(), face.top(), face.width(), face.height()
                    
                    # Redimensionamos el rostro
                    face = cv2.resize(frame[y:y + h, x:x + w], (224, 224))

                    # Guardamos el rostro capturado en una carpeta llamada 'data'
                    cv2.imwrite(path_img + '/rostros_{}.jpg'.format(document_number), face)

                # Iteramos sobre el rostro para determinar sus dimensiones y coordenadas
                for face in faces:
                    x, y, w, h = face.left(), face.top(), face.width(), face.height()
                    
                    # Redimensionamos el rostro
                    face = cv2.resize(frame[y:y + h, x:x + w], (224, 224))

                    try:
                        # Vector embedding con face-recognition
                        embedding = face_recognition.face_encodings(face)[0]

                    except Exception as e:
                        print(f"Error al identificar un rostro: {e}")

                    # Vector embedding con deepface
                    #embedding = DeepFace.extract_faces(face)[0]

                    # Convertimos el vector embedding en un array de bytes
                    byte_array = bytearray(struct.pack("f" * len(embedding), *embedding))
                    
                    #Trasladamos el array de bytes a un formato hexadecimal
                    hexadecimal = byte_array.hex()
                
                    # Establecemos conexión con la base de datos
                    self.database.connect()

                    # Ejecutamos la sentencia SQL para crear el registro en la base de datos
                    cursor = self.database.get_cursor()
                    cursor.execute(self.querys.insert_user(document_number, names, last_names, hexadecimal, gender))

                    # Confirmamos los cambios realizados en la base de datos
                    save = self.database.connection
                    save.commit()

                    cont +=1

                    if save:
                        print("Sentencia ejecutada correctamente.")
                    else:
                        print("No se puedo ejecutar la sentencia.")

                    # Terminamos la conexión con la base de datos
                    self.database.disconnect()

            else:
                print("No se encontro un rostro")

            # Terminamos el ciclo cuando se haya encontrado un rostro
            if cont == 1:
                break



class Recognition:

    def __init__(self):
        self.querys = Querys()
        self.database = DataBase()

        # Establecemos la dirección relativa para el almacenamiento de las imagenes
        self.path_dir = "./imgs"
        self.name_dir = "recog"

    
    def identify_user(self, faces, frame):

        # Guardamos la imagen del rostro en un directorio, de la persona que registramos en la base de datos
        path_img = os.path.join(self.path_dir, self.name_dir)
        if not os.path.exists(path_img):
            os.makedirs(path_img) 

        # Establecemos conexión con la base de datos
        self.database.connect()

        # Ejecutamos la sentencia SQL para crear el registro en la base de datos
        cursor = self.database.get_cursor()
        cursor.execute(self.querys.select_user("face", "names"))

        # Determinamos un umbral para determinar la similitud de los cosenos
        umbral = 0.93

        # Creamos una variable donde almacenaremos el nombre de la persona identifcada
        user_identified = None

        for face in faces:

            x, y, w, h = face.left(), face.top(), face.width(), face.height()
        
            # Redimensionamos el rostro
            face = cv2.resize(frame[y:y + h, x:x + w], (224, 224))

            # Vector embedding con face-recognition
            embedding = face_recognition.face_encodings(face)[0]

            # Iteramos sobre los registros de la base de datos
            for i in cursor:
                
                # Transformamos el vector 'embedding' de la base de datos a su formato normal
                hexadecimal = i[0].decode('utf-8')
                byte_array = bytearray.fromhex(hexadecimal)
                embedding_db = struct.unpack("f" * (len(byte_array) // 4), byte_array)

                # Determinamos la similitud de los cosenos
                #similarity = 1 - cosine(embedding, embedding_db)

                product_point = np.dot(embedding, embedding_db)

                norm_v1 = np.linalg.norm(embedding)
                norm_v2 = np.linalg.norm(embedding_db)

                similarity = product_point / (norm_v1 * norm_v2)

                # Si la similitud de los cosenos es superior al umbral imprimimos el nombre de la persona
                if similarity > umbral:
                    # print("¡Rostro encontrado! Similitud de coseno:", similarity)
                    user_identified = i[1]
                    # Guardamos el rostro capturado en una carpeta llamada 'data'
                    cv2.imwrite(path_img + '/rostros_{}.jpg'.format(i[1]), face)
                
        print(user_identified)

        # Terminamos la conexión con la base de datos
        self.database.disconnect()


    def catch_face(self):

        # Iniciamos la captura de frames en tiempo real
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        # cap = cv2.VideoCapture('rtsp://admin:53naDev@@192.168.1.108:554')

        # Cargamos el modelo de dlib para reconocer los rostros en las imagenes
        detector = dlib.get_frontal_face_detector()

        while True:

            ret, frame = cap.read()
            if ret == False:
                break
            
            # Convertimos la imagen a escala de grises
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector(gray)
            # cv2.imshow('Real Time', gray)

            # Generamos un try-exception para manejar las errores
            try:
                # Invocamos el método para que determine la identidad de la persona
                self.identify_user(faces, frame)

            except Exception as e:
                print(f"Error al identificar un rostro: {e}")

            #cv2.imshow('frame', frame)

            k = cv2.waitKey(1)
            if k == 32:
                break

        # Liberamos la fuente de vídeo y cerramos las ventanas de OpenCV
        cap.release()
        cv2.destroyAllWindows()