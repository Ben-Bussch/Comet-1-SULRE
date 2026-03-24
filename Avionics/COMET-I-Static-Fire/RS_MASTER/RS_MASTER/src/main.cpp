#include <Arduino.h>
#include <HardwareSerial.h>
#include "pressure_functions.h"
#include "Engine_functions.h"
#include <Servo.h>
#include <Wire.h>


const int RS_DE_RE_SLAVE = 10;
unsigned long lastSensorReadTime = 0;
const unsigned long SENSOR_READ_INTERVAL_MS = 50;

// Fire/Fill sequence variables
int PyroPin = 21;
int FillSequPin = 36;
int FirePin = 34;

int fireSeq = 0;
int fillSeq = 0;

int FireStartTime = 0;
int FillStartTime = 0;
int filltime = 0;
int launchtime = 0;

float pressure = 0;



// RS485 transmit helper
void sendString(const String& data) {
    digitalWrite(RS_DE_RE_SLAVE, HIGH);  // switch to transmit
    delayMicroseconds(100);

    Serial2.print(data);
    Serial2.print('\n');
    Serial2.flush();

    delayMicroseconds(100);
    digitalWrite(RS_DE_RE_SLAVE, LOW);   // back to receive
}



int clk_time = 0;
int FireStartTime = 0;
int launchtime = 0;
float pressure = 0;

String firingpinstatus = "";
String fillpinstatus = "";


//--------------- My good'ol rs485 -------------------------

void setup() {
    Serial.begin(9600);
    Serial2.begin(9600);

    pinMode(RS_DE_RE_SLAVE, OUTPUT);
    digitalWrite(RS_DE_RE_SLAVE, LOW);   // default receive

    Serial.println(SetupCurrentSensor());
    Serial.println("RS485 Slave ready.");
    SetupControl(PyroPin, FirePin, FillSequPin);
}

void loop() {
    
  clk_time = millis();


  if(clk_time%50 == 0){
   pressure = ReadPressureTransducer();
   if(Serial2.available()){
    sendString(String(pressure, 3));
   }
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


    launchtime = fireSequence(FireStartTime, clk_time, fireSeq, PyroPin);
    if(launchtime%1000 == 0){
        sendString(String(launchtime/1000));
    }
  }
  
  unsigned long currentMillis = millis();

    // ---- Update sensor readings (globals only, non-blocking) ----
    if (currentMillis - lastSensorReadTime >= SENSOR_READ_INTERVAL_MS) {
        ReadPressureTransducer();  // updates pressure_readingglobal & current_readingglobal
        lastSensorReadTime = currentMillis;
    }
        
  

}

   
        
          
              

