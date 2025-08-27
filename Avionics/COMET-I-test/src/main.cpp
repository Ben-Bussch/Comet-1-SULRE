#include <Arduino.h>
#include <Servo.h>
#include <Adafruit_INA219.h>
#include "SD.h"

//Servos
Servo NoxEngServo;
Servo IPAEngServo;
Servo FillServo;
int NoxEngPin = 6;
int IPAEngPin = 9;
int FillPin = 10;

int NoxEngStartPPM = 1050;
int IPAEngStartPPM = 1400;


int deltaPPM = 800;

int pos = 0; 
int count = 0;

//SD
const int mchipSelect = BUILTIN_SDCARD;

//Pressure sensors
Adafruit_INA219 ina219A;
Adafruit_INA219 ina219B;
Adafruit_INA219 ina219C;
Adafruit_INA219 ina219D;
float ina219intercept = -23.194;
float ina219gradient = 6.116;


void setup()
{
  // initialize LED digital pin as an output.
  pinMode(LED_BUILTIN, OUTPUT);
  // turn the LED on (HIGH is the voltage level)
  digitalWrite(LED_BUILTIN, HIGH);
  

  //Servos
  NoxEngServo.attach(NoxEngPin);
  NoxEngServo.writeMicroseconds(NoxEngStartPPM); 

  IPAEngServo.attach(IPAEngPin);
  IPAEngServo.writeMicroseconds(IPAEngStartPPM); 

  
}

void fireSequence()
{

  NoxEngServo.writeMicroseconds(NoxEngStartPPM+deltaPPM);
  IPAEngServo.writeMicroseconds(IPAEngStartPPM+deltaPPM);

}

void fillSequence()
{

  NoxEngServo.writeMicroseconds(NoxEngStartPPM);

}


void loop()
{
  /*  
  if(count < 1){
    fillSequence();
    delay(10000)
    fireSequence();
    count ++;
  }
  */ 
  

}

