#include <Arduino.h>
#include <Adafruit_INA219.h>
#include <Wire.h>
#include <PT.h>

//Pressure sensors
Adafruit_INA219 ina219A;
Adafruit_INA219 ina219B;
Adafruit_INA219 ina219C;
Adafruit_INA219 ina219D;
float ina219intercept = -23.9;
float ina219gradient = 4.9;
float p_max = 0;
float p_avg = 0;


String SetupCurrentSensor()
{
  String status;
  // Starting ina
  if (! ina219A.begin()) {
    status = "Failed to find INA219A chip";
    //Serial.println("Failed to find INA219A chip");
  }
  ina219A.setCalibration_32V_1A();
  status = "Successfully connected to INA219A chip";
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
  return status;
}

float CurrentToPressure(float current, float intercept, float grad)
{
  return current * grad + intercept;
}

float ReadPressureTransducer()
{
  //Serial.println("S");
  float currentmA = ina219A.getCurrent_mA();
  //float currentA = 1 * ina219A.getCurrent_mA();
  //Serial.println("GotCurrent");
  // float currentB = ina219B.getCurrent_mA();
  // float currentC = ina219C.getCurrent_mA();
  // float currentD = ina219D.getCurrent_mA();
  //Serial.print("A");Serial.println(currentA);
  // data1.pressure2 = CurrentToPressure(currentB, ina219BOffset, ina219BScale);
  // data1.pressure3 = CurrentToPressure(currentC, ina219COffset, ina219CScale);
  // data1.pressure4 = CurrentToPressure(currentD, ina219DOffset, ina219DScale);
  float pressure_reading = CurrentToPressure(currentmA, ina219intercept, ina219gradient);
  
  return pressure_reading;

}