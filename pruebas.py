
import serial
import time

ojo_der_x=str(100)
ojo_der_y=str(100)
ojo_izq_x="100"
ojo_izq_y=str(100)
ceja_der=str(100)
ceja_izq=str(100)
boca_abrir=str(100)
boca_del=str(100)
PuertoSerie = serial.Serial('COM8', 9600)
while True:
    boca_abrir = str(100)
    dato=ojo_der_x+ojo_der_y+ojo_izq_x+ojo_izq_y+ceja_der+ceja_izq+boca_abrir+boca_del+"1"
    PuertoSerie.write(dato.encode())
    time.sleep(2)
    PuertoSerie.write(b'\n')
    time.sleep(2)
    boca_abrir = str(150)
    dato = ojo_der_x + ojo_der_y + ojo_izq_x + ojo_izq_y + ceja_der + ceja_izq + boca_abrir + boca_del + "1"
    PuertoSerie.write(dato.encode())
    time.sleep(2)
    PuertoSerie.write(b'\n')
    time.sleep(5)
