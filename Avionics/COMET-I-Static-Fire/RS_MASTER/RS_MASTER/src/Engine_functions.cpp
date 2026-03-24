#include <Arduino.h>
#include <Servo.h>
#include <Wire.h>
#include "Engine_functions.h"

Servo NoxEngServo;
Servo IPAEngServo;
Servo FillServo;

int NoxEngPin = 6;
int IPAEngPin = 9;
int FillPin = 11;


int NoxEngStartPPM = 1050;
int IPAEngStartPPM = 1400;
int FillStartPPM = 1050;


int NoxdeltaPPM = 800;
int IPAdeltaPPM = 600;
int FilldeltaPPM = 750;

int PPMpos = 0; 
int count = 0;

void SetupControl(int PyroPin, int FirePin, int FillSequPin){
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

void Rest(){
   NoxEngServo.writeMicroseconds(NoxEngStartPPM);
   IPAEngServo.writeMicroseconds(IPAEngStartPPM); 
   FillServo.writeMicroseconds(FillStartPPM); 
}
int fillSequence(int FillStartTime, int clk_time, int fillSeq)
{
  int filltime = - FillStartTime + clk_time;
  
  if(fillSeq == 0){
      NoxEngServo.writeMicroseconds(NoxEngStartPPM);
      IPAEngServo.writeMicroseconds(IPAEngStartPPM);
      FillServo.writeMicroseconds(FillStartPPM);
      PPMpos = 0;
      fillSeq = 1;
  }
  if(fillSeq == 1 && filltime%5 == 0){
    // waits 5ms for the servo to reach the position
    while(PPMpos <= (FilldeltaPPM)){
      PPMpos += 3;
      FillServo.writeMicroseconds(PPMpos+FillStartPPM); 
    }
    if(PPMpos >= (FilldeltaPPM)){
      fillSeq = 2;  
    }

    return filltime;
  }
  



}


int fireSequence(int FireStartTime, int clk_time, int FireSeq, int PyroPin)
{
  int countdown = - 10000 - FireStartTime + clk_time;

  if(FireSeq == 0){
      FillServo.writeMicroseconds(FillStartPPM);
      FireSeq = 1;
  }


  if(clk_time -  FireStartTime  >= 10000 && FireSeq == 1){
    digitalWrite(PyroPin, HIGH);
    FireSeq = 2; 
  }

  if(clk_time -  FireStartTime  >= 10100 && FireSeq == 2){
    NoxEngServo.writeMicroseconds(NoxEngStartPPM+NoxdeltaPPM); 
    FireSeq = 3; 
  }
 if(clk_time -  FireStartTime  >= 10200 && FireSeq == 3){
    IPAEngServo.writeMicroseconds(IPAEngStartPPM+IPAdeltaPPM);
    FireSeq = 4; 
  }

  return countdown;
}

