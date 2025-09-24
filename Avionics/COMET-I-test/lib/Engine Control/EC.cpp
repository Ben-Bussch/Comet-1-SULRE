#include <Arduino.h>
#include <Servo.h>
#include <Wire.h>

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

void SetupControl(){
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


int fireSequence(int FireStartTime, int clk_time, int FireSeq)
{
  int countdown = - 10000 - FireStartTime + clk_time;

  if(FireSeq = 0){
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

