#include <Servo.h>
#include <stdlib.h>
Servo ojo_der_x;
Servo ojo_der_y;
Servo ojo_izq_x;
Servo ojo_izq_y;
Servo ceja_der;
Servo ceja_izq;
Servo boca_abrir;
Servo boca_del;
float valor;
char mover_boca='0', mover_boca_a='0';;

void setup()
{
  Serial.begin(9600);
  //Pines de cada servo
  ojo_der_x.attach(0);
  ojo_der_y.attach(1);
  ojo_izq_x.attach(2);
  ojo_izq_y.attach(3);
  ceja_der.attach(4);
  ceja_izq.attach(5);
  boca_abrir.attach(6);
  boca_del.attach(7);

  ojo_der_x.write(100);   //0 a 200
  ojo_der_y.write(100);   //0 a 200

  ojo_izq_x.write(100);   //0 a 200
  ojo_izq_y.write(100);   //0 a 200

  ceja_der.write(100);  //100 a 0
  ceja_izq.write(100);   //100 a 200
  
  boca_del.write(125);   //100 a 150
  boca_abrir.write(70); //20 a 120
}

void loop()
{
  mover_boca = Serial.read();

  while(mover_boca=='1'){
  valor=random(0,100);
  boca_del.write((valor/100)*50+100);   //100 a 150
  boca_abrir.write((valor/100)*100+20); //20 a 120
  delay(200);
  if(Serial.read()=='0'){mover_boca=0;}
  }
  boca_del.write(125);   //100 a 150
  boca_abrir.write(70); //20 a 120
  delay(200);
  /*

  valor = analogRead(A0);
  Serial.println(valor);

  ojo_der_x.write((valor/1023)*200);   //0 a 200
  ojo_der_y.write((valor/1023)*200);   //0 a 200

  ojo_izq_x.write((valor/1023)*200);   //0 a 200
  ojo_izq_y.write((valor/1023)*200);   //0 a 200

  ceja_der.write(-(valor/1023)*100+100);  //100 a 0
  ceja_izq.write((valor/1023)*100+100);   //100 a 200
  
  boca_del.write((valor/1023)*50+100);   //100 a 150
  boca_abrir.write((valor/1023)*100+20); //20 a 120
  delay(200);
  */
  
 
}
