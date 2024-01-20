import face_recognition
import cv2
import numpy as np
import serial
import time
import pyttsx3 as voz
import speech_recognition as sr

import openai  # pip install openai
from rich import print  # pip install rich



ojo_der_x=str(100)
ojo_der_y=str(100)
ojo_izq_x=str(100)
ojo_izq_y=str(100)
ceja_der=str(100)
ceja_izq=str(100)
boca_abrir=str(120)
boca_del="150"



PuertoSerie = serial.Serial('COM8', 9600)

openai.api_key = "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"
# Contexto del asistente
context = {"role": "system",
            "content": "Eres una cabeza robótica llamada Animatrón."}
messages = [context]

#Creamos la voz
voice = voz.init()
voices = voice.getProperty('voices')
voice.setProperty('voice', voices[0].id)
voice.setProperty('rate', 140)

def say(text):
    boca_abrir="aaa"
    dato = ojo_der_x + ojo_der_y + ojo_izq_x + ojo_izq_y + ceja_der + ceja_izq + boca_abrir + boca_del + "1"+"\n"
    PuertoSerie.write(dato.encode())
    voice.say(text)
    voice.runAndWait()
    dato = "bbb"+"\n"
    PuertoSerie.write(dato.encode())


# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Load a sample picture and learn how to recognize it.
obama_image = face_recognition.load_image_file("obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# Load a second sample picture and learn how to recognize it.
biden_image = face_recognition.load_image_file("biden.jpg")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    obama_face_encoding,
    biden_face_encoding
]
known_face_names = [
    "Barack Obama",
    "Joe Biden"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
reconocido = False

encontrado=0
while not reconocido:
    boca_abrir = str(120)
    boca_del = "150"
    PuertoSerie.write(b'\n')
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    face_names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        print("Los matches son:\n")
        print(matches)
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
            reconocido=True
            say("Hola "+ known_face_names[matches.index(True)])
            cara=known_face_names[matches.index(True)]
            encontrado=1
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index] and encontrado==0:
            name = known_face_names[best_match_index]
            reconocido = True
            say("Hola " + known_face_names[matches.index(True)])
            cara=known_face_names[matches.index(True)]
            encontrado=2
        if encontrado==0:
            known_face_encodings.append(face_encodings[0])
            print("Identificado")
            say("Hola, ¿cómo te llamas?")
            PuertoSerie.write(b'\n')
            while not reconocido:
                try:
                    recognizer = sr.Recognizer()
                    with sr.Microphone() as source:
                        print("Escuchando...")
                        audio = recognizer.listen(source, phrase_time_limit=2)
                        print("Escuchado")
                        comando = recognizer.recognize_google(audio, language='es-ES')
                        print("Creo que dijiste: " + comando)

                        known_face_names.append(str(comando))
                        reconocido = True
                        say("Encantado de conocerte,"+comando)
                        cara=comando
                except:
                    say("No te he entendido")




top = 152
right = 324
bottom = 296
left = 180

while True:
    boca_abrir = str(120)
    boca_del = "150"
    PuertoSerie.write(b'\n')
    # Grab a single frame of video
    ret, frame = video_capture.read()
    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_small_frame)
    #face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    face_names = []
    name=cara

    # Display the results
    # Scale back up face locations since the frame we detected in was scaled to 1/4 size
    top_A = top
    right_A = right
    bottom_A = bottom
    left_A = left
    try:
        top = face_locations[0][0]
        right = face_locations[0][1]
        bottom = face_locations[0][2]
        left = face_locations[0][3]
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
    except IndexError:
        top = top_A
        right = right_A
        bottom = bottom_A
        left = left_A


    print(top, right, bottom, left)

    # Draw a box around the face
    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
    punto = np.array([left + (right - left) / 2, top + (bottom - top) / 2])  # En x,y
    centro = np.array([325, 250])  # x,y
    diferencia = punto - centro
    dato = ojo_der_x + ojo_der_y + ojo_izq_x + ojo_izq_y + ceja_der + ceja_izq + boca_abrir + boca_del
    calculo = np.array([100 - diferencia[0] * 100 / centro[0], 100 + diferencia[1] * 100 / centro[1]])
    # Draw a label with a name below the face
    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
    font = cv2.FONT_HERSHEY_DUPLEX
    cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    print("Datos:")
    print(diferencia)
    print(calculo)

    enviar = np.array([str(int(calculo[0])), str(int(calculo[1]))])
    enviar2 = np.array(["000", "000"])
    print(enviar)
    if calculo[0] < 10:
        enviar2[0] = "00" + enviar[0]
    elif calculo[0] < 100 and calculo[0] > 10:
        enviar2[0] = "0" + enviar[0]
    else:
        enviar2[0] = enviar[0]
    if calculo[1] < 10:
        enviar2[1] = "00" + enviar[1]
    elif calculo[1] < 100 and calculo[1] > 10:
        enviar2[1] = "0" + enviar[1]
    else:
        enviar2[1] = enviar[1]
    ojo_der_x = str(enviar2[0])
    ojo_der_y = str(enviar2[1])
    ojo_izq_x = str(enviar2[0])
    ojo_izq_y = str(enviar2[1])
    print(enviar2)
    dato = ojo_der_x + ojo_der_y + ojo_izq_x + ojo_izq_y + ceja_der + ceja_izq + boca_abrir + boca_del + "1"
    PuertoSerie.write(dato.encode())
    time.sleep(0.1)
    # PuertoSerie.write(b'\n')



    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Hit 's' on the keyboard to speak!
    if cv2.waitKey(1) & 0xFF == ord('s'):
        recognizer = sr.Recognizer()
        # Activar microfono
        with sr.Microphone() as source:
            print("Escuchando...")
            audio = recognizer.listen(source, phrase_time_limit=5)

        try:
            comando = recognizer.recognize_google(audio, language='es-ES')
            print("Creo que dijiste: " + comando)

            PuertoSerie.write(b'\n')
            ceja_izq = "150"
            dato = ojo_der_x + ojo_der_y + ojo_izq_x + ojo_izq_y + ceja_der + ceja_izq + boca_abrir + boca_del + "1" + "\n"
            PuertoSerie.write(dato.encode())
            content = comando
            messages.append({"role": "user", "content": content})
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=messages)
            response_content = response.choices[0].message.content
            ceja_der = str(100)
            ceja_izq = str(100)
            dato = ojo_der_x + ojo_der_y + ojo_izq_x + ojo_izq_y + ceja_der + ceja_izq + boca_abrir + boca_del + "1" + "\n"
            PuertoSerie.write(dato.encode())
            say(response_content)


        except:
            say("No te he entendido")
            ceja_izq = "100"



# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()


# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
