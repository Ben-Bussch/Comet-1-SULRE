#include <Arduino.h>
#include <Servo.h>
#include <Adafruit_INA219.h>
#include "SD.h"
#include <Wire.h>
#include <PT.cpp>
#include <EC.cpp>
//#include <SoftwareSerial.h>

int fireSeq = 0;
int fillSeq = 0;

int clk_time = 0;
int FireStartTime = 0;
int FillStartTime = 0;
int filltime = 0;
int launchtime = 0;
float pressure = 0;
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

  SetupControl();  
}




void loop()
{
  clk_time = millis();


  if(clk_time%50 == 0){
   pressure = ReadPressureTransducer();
  }
  /*if(clk_time%500 == 0){
   Serial.println(pressure);
  }*/


  if (digitalRead(FillSequPin) == LOW && digitalRead(FirePin) == LOW ){
    Rest();
    fillSeq = 0;
  }

  if (digitalRead(FillSequPin) == HIGH && digitalRead(FirePin) == LOW){
      filltime = fillSequence(FillStartTime, clk_time, fillSeq);
      if(filltime%10000 == 0){
        Serial.println(launchtime/1000);
    }
  }

  
  if (digitalRead(FirePin) == LOW){
    //Serial.println("Fire is LOW");
    digitalWrite(PyroPin, LOW);
    fireSeq = 0;
    FireStartTime = clk_time;
  }

  if (digitalRead(FirePin) == HIGH && digitalRead(FillSequPin) == HIGH){
    //Serial.println("Fire is HIGH");
    fillSeq = 0; //get out of fill sequence


    launchtime = fireSequence(FireStartTime, clk_time, fireSeq);
    if(launchtime%1000 == 0){
        Serial.println(launchtime/1000);
    }
  }


}

