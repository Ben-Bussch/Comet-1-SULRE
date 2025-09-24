#include <Arduino.h>
#include <Servo.h>
#include <Adafruit_INA219.h>
#include "SD.h"
#include <Wire.h>
#include <PT.cpp>
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

//Control
int PyroPin = 21;
int FillSequPin = 36;
int FirePin = 34;
int clk_time = 0;



//SD
const int mchipSelect = BUILTIN_SDCARD;



void setup()
{
  // turn the LED on (HIGH is the voltage level)
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);

  Serial.begin(115200);
  while (!Serial && millis() < 5000) {}
  //Serial.begin(9600); 
  Serial.println("Hello from Teensy 4.1!");

  String PT_status = SetupCurrentSensor();
  Serial.println(PT_status);
  
  //Servos
  NoxEngServo.attach(NoxEngPin);
  NoxEngServo.writeMicroseconds(NoxEngStartPPM); 

  IPAEngServo.attach(IPAEngPin);
  IPAEngServo.writeMicroseconds(IPAEngStartPPM); 

  FillServo.attach(FillPin);
  FillServo.writeMicroseconds(FillStartPPM); 

  //Inputs and Outputs
  pinMode(PyroPin, OUTPUT);

  pinMode(FirePin, INPUT);
  pinMode(FillSequPin,  INPUT);

  
}

void fireSequence()
{
  FillServo.writeMicroseconds(FillStartPPM);
  delay(5000); 
  NoxEngServo.writeMicroseconds(NoxEngStartPPM+NoxdeltaPPM);
  delay(100); 
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
  clk_time = millis();
  

  float pressure = ReadPressureTransducer();
  if(pressure > p_max){
    p_max = pressure;    
  }
  p_avg += pressure;

  if(millis()%1000 == 0){
    p_avg = p_avg/1000;
    //Serial.println(p_avg);
    p_avg = 0;
  }


  if (digitalRead(FillSequPin) == HIGH){
    Serial.println("Fill is HIGH");
  }

  if (digitalRead(FirePin) == HIGH){
    Serial.println("Fire is HIGH");
    digitalWrite(PyroPin, HIGH);
  }

  if (digitalRead(FirePin) == LOW){
    Serial.println("Fire is LOW");
    digitalWrite(PyroPin, LOW);
  }
  
    
    
  


  
  //Serial.println(p_max);

  //Serial.println("Hello from Teensy 4.1!");
  
    /*
    if(count < 1){
    delay(1000);
    fillSequence();
    //FillServo.writeMicroseconds(FillStartPPM);
    delay(20000);
    fireSequence();
    //FillServo.writeMicroseconds(FillStartPPM+FilldeltaPPM);
    
    count ++;
   
  }
  */
  

}

