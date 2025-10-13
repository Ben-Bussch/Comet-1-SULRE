


#include <Arduino.h>
#include <HardwareSerial.h>
#include "pressure_functions.h"
//#include "EC.h"
#include <Servo.h>
#include <Wire.h>


const int RS_DE_RE_SLAVE = 10;
unsigned long lastSensorReadTime = 0;
const unsigned long SENSOR_READ_INTERVAL_MS = 50;

// Fire/Fill sequence variables
int fireSeqState = -1;   // -1 means idle
unsigned long fireStartTime = 0;

// RS485 transmit helper
void sendString(const String& data) {
    digitalWrite(RS_DE_RE_SLAVE, HIGH);  // switch to transmit
    delayMicroseconds(100);

    Serial2.print(data);
    Serial2.print('\n');
    Serial2.flush();

    delayMicroseconds(1-0);
    digitalWrite(RS_DE_RE_SLAVE, LOW);   // back to receive
}
//----------------- Ben servo stuff --------------------
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

int fireSeq = 0;
int fillSeq = 0;

int clk_time = 0;
int FireStartTime = 0;
int launchtime = 0;
float pressure = 0;

String firingpinstatus = "";
String fillpinstatus = "";


//----------------- Ben Control stuff ( i think sequencing) ------------------------------
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

void Rest(){
   NoxEngServo.writeMicroseconds(NoxEngStartPPM);
   IPAEngServo.writeMicroseconds(IPAEngStartPPM); 
   FillServo.writeMicroseconds(FillStartPPM); 
}
void fillSequence()
{

  NoxEngServo.writeMicroseconds(NoxEngStartPPM);
  IPAEngServo.writeMicroseconds(IPAEngStartPPM);
  
  FillServo.writeMicroseconds(FillStartPPM);
  for (PPMpos = 0; PPMpos <= (FilldeltaPPM); PPMpos += 1) { // goes from 0 degrees to 180 degrees in steps of 1 ppm
    FillServo.writeMicroseconds(PPMpos+FillStartPPM);// tell servo to go to position in variable 'pos'
    delay(5);                       
  }

}




int fireSequence(int FireStartTime, int clk_time, int FireSeq)
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


//--------------- My good'ol rs485 -------------------------

void setup() {
    Serial.begin(9600);
    Serial2.begin(9600);

    pinMode(RS_DE_RE_SLAVE, OUTPUT);
    digitalWrite(RS_DE_RE_SLAVE, LOW);   // default receive

    Serial.println(SetupCurrentSensor());
    Serial.println("RS485 Slave ready.");
    SetupControl();
}

void loop() {
    
  clk_time = millis();


  if(clk_time%50 == 0){
   pressure = ReadPressureTransducer();
  }
  /*if(clk_time%500 == 0){
   Serial.println(pressure);
  }*/


  if (digitalRead(FillSequPin) == LOW ){
    Rest();
    fillSeq = 0;
  }

  if (digitalRead(FillSequPin) == HIGH && digitalRead(FirePin) == LOW){
    if(fillSeq == 0){
      fillSequence();
      fillSeq = 1;
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
    launchtime = fireSequence(FireStartTime, clk_time, fireSeq);
    firingpinstatus = digitalRead(FirePin);
    fillpinstatus = digitalRead(FillSequPin);
    if(launchtime%1000 == 0){
        Serial.println(launchtime/1000);
    }
  }
  
  unsigned long currentMillis = millis();

    // ---- Update sensor readings (globals only, non-blocking) ----
    if (currentMillis - lastSensorReadTime >= SENSOR_READ_INTERVAL_MS) {
        ReadPressureTransducer();  // updates pressure_readingglobal & current_readingglobal
        lastSensorReadTime = currentMillis;
    }

    // ---- Handle incoming RS485 commands ----
    while (Serial2.available()) {
        String cmd = Serial2.readStringUntil('\n');
        cmd.trim();

        if (cmd.equalsIgnoreCase("alive")) {
            sendString("I am alive");
        } 
        else if (cmd.equalsIgnoreCase("PRESS?")) {
            sendString(String(pressure, 3));
        } 
        else if (cmd.equalsIgnoreCase("FIRE")) {
          sendString("Fire sequence started");  // send first
          fireStartTime = currentMillis;
          fireSeqState = 0;  // reset fire sequence
        }
        else if (cmd.equalsIgnoreCase("FILL")) {
          sendString("Fill sequence executed");  // send first
          fillSequence();                         // then run the fill
        }
    
         
        while(digitalRead(FirePin)== HIGH){
        

            sendString("Firing sequence active)");
        

          }
    }
      
    
    
    // ---- Fire sequence non-blocking ----
    if (fireSeqState >= 0) {
        fireSequence(fireStartTime, currentMillis, fireSeqState);
        fireSeqState++;   // advance sequence step
        if (fireSeqState > 4) {  // adjust based on your sequence steps
            fireSeqState = -1;    // finished
        }
    }
}

   
        
          
              

