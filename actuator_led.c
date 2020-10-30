#include <Wire.h>
#define SLAVE_ADDRESS 0x06
#define LED A2

int stage = 0;
int x = 0;
int instr_number;
void setup(void) {
  pinMode(LED, OUTPUT);
  Serial.begin(9600);
  Wire.begin(SLAVE_ADDRESS);
  Serial.println("I2C Ready!");
  Serial.println("LED experiment!");
  Wire.onReceive(receiveData);
}
  
void loop(){
}
void receiveData(int byteCount){
  while(Wire.available()) {
    instr_number = Wire.read();
    Serial.print("data received: ");
    Serial.println(instr_number);
    if (instr_number == 1){
      sendType();
    }
    if (instr_number == 2){
      on();
      Serial.println("불이 켜집니다");
    }

    else if (instr_number == 3){
      off();
      Serial.println("불이 꺼집니다.");
    }
    else{
      Stage();
    }
  }
}
void sendType() {
  int type = 2;
  Wire.write((int)type);
}
void on() {
  digitalWrite(LED, HIGH);
  Serial.println("on");
}
void off(){
  digitalWrite(LED, LOW);
  Serial.println("off");
}
void Stage(){
  if (instr_number == 0){
    stage = stage/10;
    Serial.println(stage);
    if (stage == 0){
      Serial.println("작동안함");
    }
    else if(stage == 1){
      Serial.println("작동안함");
    }
    else if(stage>=1){
      x = x+50;
      if (255<x){
      x = 255;
    }
    Serial.println("상승");
    analogWrite(LED, x);
    }
    else{
    x = x-50;
    if (x<0){
      x = 0;
    }
    Serial.println("하강");
    analogWrite(LED, x);
    }
     stage = 0;
  }
  else{
   stage = 0-stage - instr_number;
  }
}
