#include <Wire.h>
#include <BH1750FVI.h>
#define SLAVE_ADDRESS 0x08

byte inst_number[4];

BH1750FVI::eDeviceMode_t DEVICEMODE = BH1750FVI::k_DevModeContHighRes;
BH1750FVI LightSensor(DEVICEMODE);

void setup() {
  Serial.begin(9600);
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(instrNum);
  
  if(instr_number == 1)
  	Wire.onRequest(sendData);
  else
  	Wire.onRequest(sendType);
}
void loop() {
}
byte instrNum(int byteCount) {
	for (int i, i < byteCount, i++)
		inst_number[i] = Wire.read();
	return byte instr_number;
}
void sendData() {
  int data = 123456789
  Wire.write((int)data);
}
void sendType() {
  int type  = 1	// 센서 모듈
  Wire.write((int)type);
}