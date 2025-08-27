#include <Arduino.h>
#include <Servo.h>
#include <Adafruit_INA219.h>
#include "SD.h"
//#include <SoftwareSerial.h>

//Servos
Servo NoxEngServo;
Servo IPAEngServo;
Servo FillServo;
int NoxEngPin = 6;
int IPAEngPin = 9;
int FillPin = 10;

int NoxEngStartPPM = 1050;
int IPAEngStartPPM = 1400;
int FillStartPPM = 1050;


int NoxdeltaPPM = 800;
int IPAdeltaPPM = 600;
int FilldeltaPPM = 750;

int PPMpos = 0; 
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


void SetupCurrentSensor()
{
  // Starting ina
  if (! ina219A.begin()) {
    Serial.println("Failed to find INA219A chip");
    while (1);
  }
  ina219A.setCalibration_32V_1A();
  // if (! ina219B.begin()) {
  //   Serial.println("Failed to find INA219B chip");
  //   while (1);
  // }
  // ina219B.setCalibration_32V_1A();
  // if (! ina219C.begin()) {
  //   Serial.println("Failed to find INA219C chip");
  //   while (1);
  // }
  // ina219C.setCalibration_32V_1A();
  // if (! ina219D.begin()) {
  //   Serial.println("Failed to find INA219D chip");
  //   while (1);
  // }
  // ina219D.setCalibration_32V_1A();
}

float CurrentToPressure(float current, float intercept, float grad)
{
  return current * grad + intercept;
}

void ReadPressureTransducer()
{
  //Serial.println("S");
  float currentA = -1 * ina219A.getCurrent_mA();
  //Serial.println("GotCurrent");
  // float currentB = ina219B.getCurrent_mA();
  // float currentC = ina219C.getCurrent_mA();
  // float currentD = ina219D.getCurrent_mA();

  Serial.println(CurrentToPressure(currentA, ina219intercept, ina219gradient));
  //Serial.print("A");Serial.println(currentA);
  // data1.pressure2 = CurrentToPressure(currentB, ina219BOffset, ina219BScale);
  // data1.pressure3 = CurrentToPressure(currentC, ina219COffset, ina219CScale);
  // data1.pressure4 = CurrentToPressure(currentD, ina219DOffset, ina219DScale);
}

void setup()
{

  pinMode(LED_BUILTIN, OUTPUT);
  // turn the LED on (HIGH is the voltage level)
  digitalWrite(LED_BUILTIN, HIGH);


  Serial.begin(9600); 
  Serial.println("Hello from Teensy 4.1!");
  // initialize LED digital pin as an output.
  
  

  //Servos
  NoxEngServo.attach(NoxEngPin);
  NoxEngServo.writeMicroseconds(NoxEngStartPPM); 

  IPAEngServo.attach(IPAEngPin);
  IPAEngServo.writeMicroseconds(IPAEngStartPPM); 

  FillServo.attach(FillPin);
  FillServo.writeMicroseconds(FillStartPPM); 

  
}

void fireSequence()
{
  FillServo.writeMicroseconds(FillStartPPM);
  delay(5000); 
  NoxEngServo.writeMicroseconds(NoxEngStartPPM+NoxdeltaPPM);
  IPAEngServo.writeMicroseconds(IPAEngStartPPM+IPAdeltaPPM);

}

void fillSequence()
{

  NoxEngServo.writeMicroseconds(NoxEngStartPPM);
  IPAEngServo.writeMicroseconds(IPAEngStartPPM);
  
  FillServo.writeMicroseconds(FillStartPPM);
  for (PPMpos = 0; PPMpos <= (FilldeltaPPM); PPMpos += 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 ppm
    FillServo.writeMicroseconds(PPMpos+FillStartPPM);              // tell servo to go to position in variable 'pos'
    delay(5);                       // waits 5ms for the servo to reach the position
  }

}


void loop()
{
  ReadPressureTransducer();
  
  /*
    if(count < 1){
    delay(1000);
    //fillSequence();
    FillServo.writeMicroseconds(FillStartPPM);
    delay(60000);
    //fireSequence();
    FillServo.writeMicroseconds(FillStartPPM+FilldeltaPPM);
    
    count ++;
  }
  */ 

  
  

}

