// #include <Arduino.h>
// #include <HardwareSerial.h>
// #include "pressure_functions.h" 


// const int RS_DE_RE_SLAVE = 10;


// void sendString(const String& data) {
//   // 1. Switch to transmit mode
//   digitalWrite(RS_DE_RE_SLAVE, HIGH);
//   delayMicroseconds(50);

//   // 2. Send the data with a newline terminator
//   Serial2.print(data);
//   Serial2.print('\n');
//   Serial2.flush();

//   // 3. Switch back to receive mode
//   delayMicroseconds(50);
//   digitalWrite(RS_DE_RE_SLAVE, LOW);
// }

// void setup() {
//   Serial.begin(9600);  
//   Serial2.begin(9600); 

//   pinMode(RS_DE_RE_SLAVE, OUTPUT);
//   digitalWrite(RS_DE_RE_SLAVE, LOW); // Default to receive mode

//   // Initialize your pressure sensor
//   String status = SetupCurrentSensor();
//   Serial.println(status);

//   // Serial.println("Pressure Slave Ready. Waiting for 'PRESS?' command...");
// }

// void loop() {
//   // Check if the master has sent a command
//   if (Serial2.available()) {
//     String command = Serial2.readStringUntil('\n');
//     command.trim();

//     // If the command is "PRESS?", read the sensor and reply
//     if (command.equalsIgnoreCase("PRESS?")) { 
//       Serial.println("PRESS?");

//       float pressure = ReadPressureTransducer();
//       String dataToSend = String(pressure, 2); // Convert to string

//       //Serial.print("Sending pressure: ");
//       //Serial.println(dataToSend);

      
//       sendString(dataToSend);
//     }
//   }
// }