#!/usr/bin/python

# Importamos la libreria de PySerial
import serial
import pyttsx3 as voz
import speech_recognition as sr
import subprocess as sub
from datetime import datetime
import openai
import time



# Abrimos el puerto de la placa a 9600
PuertoSerie = serial.Serial('COM8', 9600)

while True:
    print("Mover")
    sArduino = PuertoSerie.write(b'1')
    time.sleep(3)
    print("Parar")
    sArduino = PuertoSerie.write(b'0')
    time.sleep(3)











