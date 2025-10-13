// #include <Arduino.h>
// #include <HardwareSerial.h>
// #include "pressure_functions.h" 


// const int RS_DE_RE_SLAVE = 10;


// void sendString(const String& data) {
  
//   digitalWrite(RS_DE_RE_SLAVE, HIGH);
//   delayMicroseconds(50);

  
//   Serial2.print(data);
//   Serial2.print('\n');
//   Serial2.flush();

  
//   delayMicroseconds(100);
//   digitalWrite(RS_DE_RE_SLAVE, LOW);
// }

// void setup() {
//   Serial.begin(9600);  
//   Serial2.begin(9600); 

//   pinMode(RS_DE_RE_SLAVE, OUTPUT);
//   digitalWrite(RS_DE_RE_SLAVE, LOW); // Default to receive mode

  
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



// #include <Arduino.h>
// #include <HardwareSerial.h>
// #include "pressure_functions.h"  
// # define PRESSURE_SENSOR_CONNECTED
// const int RS_DE_RE_SLAVE = 10;

// void sendString(const String& data) {
//   // Switch to transmit mode
//   digitalWrite(RS_DE_RE_SLAVE, HIGH);
//   delay(10);                

//   Serial2.print(data);
//   Serial2.print('\n');
//   Serial2.flush();

//   delay(10);                
//   digitalWrite(RS_DE_RE_SLAVE, LOW);  
// }

// void setup() {
//   Serial.begin(9600);    
//   Serial2.begin(9600);   

//   pinMode(RS_DE_RE_SLAVE, OUTPUT);
//   digitalWrite(RS_DE_RE_SLAVE, LOW); // default to receive

//   // Initialize pressure sensor (optional)
//   String status = SetupCurrentSensor();
//   Serial.println(status);

//   // Serial.println("RS485 Slave ready. Waiting for commands...");
// }

// void loop() {
  
//   if (Serial.available()) {
//     String msg = Serial.readStringUntil('\n');
//     msg.trim();
//     if (msg.length() > 0) {
//       sendString(msg);
//       // Serial.print("Sent to bus: ");
//       // Serial.println(msg);
//     }
//   }

  
//   if (Serial2.available()) {
//     String cmd = Serial2.readStringUntil('\n');
//     cmd.trim();
//     // Serial.print("Received from bus: ");
//     Serial.println(cmd);

//     if (cmd.equalsIgnoreCase("alive")) {
//       sendString("I am alive");
//       // Serial.println("Responded with 'I am alive'");
//     } 
//     else if (cmd.equalsIgnoreCase("PRESS?")) {
// #ifdef PRESSURE_SENSOR_CONNECTED
//       float pressure = ReadPressureTransducer();
//       String dataToSend = String(pressure, 2);
//       sendString(dataToSend);
//       // Serial.print("Responded with pressure: ");
//       Serial.println(dataToSend);
// #else
//       sendString("<no data>");
//       // Serial.println("Responded with 'pressure sensor not connected'");
// #endif
//     }
//   }
// }



// #include <Arduino.h>
// #include <HardwareSerial.h>
// #include "pressure_functions.h"  

// const int RS_DE_RE_SLAVE = 10;

// void sendString(const String& data) {
//   // Switch to transmit mode
//   digitalWrite(RS_DE_RE_SLAVE, HIGH);
//   delay(50);                

//   Serial2.print(data);
//   Serial2.print('\n');
//   Serial2.flush();

//   delay(50);                
//   digitalWrite(RS_DE_RE_SLAVE, LOW);  
// }

// void setup() {
//   Serial.begin(9600);    
//   Serial2.begin(9600);   

//   pinMode(RS_DE_RE_SLAVE, OUTPUT);
//   digitalWrite(RS_DE_RE_SLAVE, LOW); // default to receive

//   // Initialize pressure sensor
//   String status = SetupCurrentSensor();
//   Serial.println(status);
// }

// void loop() {
//   // Forward any input from Serial to bus
//   if (Serial.available()) {
//     String msg = Serial.readStringUntil('\n');
//     msg.trim();
//     if (msg.length() > 0) {
//       sendString(msg);
//     }
//   }

//   // Handle incoming RS485 commands
//   if (Serial2.available()) {
//     String cmd = Serial2.readStringUntil('\n');
//     cmd.trim();
//     Serial.println(cmd); // for debugging

//     if (cmd.equalsIgnoreCase("alive")) {
//       sendString("I am alive");
//     } 
//     else if (cmd.equalsIgnoreCase("PRESS?")) {
//       // Attempt to read the pressure
//       float pressure = ReadPressureTransducer();
      
//       // Check if the reading is valid (use isnan for failure)
//       if (isnan(pressure)) {
//         sendString("<no data>");
//         Serial.println("<no data>");
//       } else {
//         String dataToSend = String(pressure, 2);
//         sendString(dataToSend);
//         Serial.println(dataToSend);
//       }
//     }
//   }
// }



// #include <Arduino.h>
// #include <HardwareSerial.h>
// #include "pressure_functions.h"


// const int RS_DE_RE_SLAVE = 10;

// #define PRESSURE_SENSOR_CONNECTED

// // Timing constants
// const unsigned long SENSOR_READ_INTERVAL_MS = 50; // how often to update pressure reading

// // Variables
// String inputBuffer = "";
// float lastPressure = 0.0;
// unsigned long lastSensorReadTime = 0;

// void sendString(const String& data) {
//   // Switch to transmit
//   digitalWrite(RS_DE_RE_SLAVE, HIGH);
//   delayMicroseconds(10);

//   Serial2.print(data);
//   Serial2.print('\n');
//   Serial2.flush();

//   delayMicroseconds(10);
//   digitalWrite(RS_DE_RE_SLAVE, LOW);
// }

// void setup() {
//   Serial.begin(9600);    
//   Serial2.begin(9600);   

//   pinMode(RS_DE_RE_SLAVE, OUTPUT);
//   digitalWrite(RS_DE_RE_SLAVE, LOW); // default to receive

// #ifdef PRESSURE_SENSOR_CONNECTED
//   String status = SetupCurrentSensor();
//   Serial.println(status);
// #endif

//   Serial.println("RS485 Slave ready.");
// }

// void loop() {
//   // ---- Non-blocking sensor reading ----
//   unsigned long currentMillis = millis();
// #ifdef PRESSURE_SENSOR_CONNECTED
//   if (currentMillis - lastSensorReadTime >= SENSOR_READ_INTERVAL_MS) {
//     lastPressure = ReadPressureTransducer();
//     lastSensorReadTime = currentMillis;
//   }
// #endif

//   // ---- Read incoming Serial2 bytes non-blocking ----
//   while (Serial2.available()) {
//     char c = Serial2.read();
//     if (c == '\n') {
//       inputBuffer.trim();
//       if (inputBuffer.length() > 0) {
//         Serial.print("Received command: ");
//         Serial.println(inputBuffer);

//         if (inputBuffer.equalsIgnoreCase("alive")) {
//           sendString("I am alive");
//         } 
//         else if (inputBuffer.equalsIgnoreCase("PRESS?")) {
// #ifdef PRESSURE_SENSOR_CONNECTED
//     // Send the last known pressure reading
//     String dataToSend = String(pressure_readingglobal, 2);
//     sendString(dataToSend);
//     Serial.println("Sent pressure: " + dataToSend);
// #else
//     sendString("<no data>");
// #endif
// }

//         }
//       }
//       inputBuffer = ""; // clear buffer
//     } else {
//       inputBuffer += c;
//     }
//   }

//   // ---- Optional: handle Serial monitor input ----
//   while (Serial.available()) {
//     char c = Serial.read();
//     if (c == '\n') {
//       inputBuffer.trim();
//       if (inputBuffer.length() > 0) {
//         sendString(inputBuffer);
//         Serial.print("Sent to bus: ");
//         Serial.println(inputBuffer);
//       }
//       inputBuffer = "";
//     } else {
//       inputBuffer += c;
//     }
//   }
// }


// #include <Arduino.h>
// #include <HardwareSerial.h>
// #include "pressure_functions.h"  // contains pressure_readingglobal

// const int RS_DE_RE_SLAVE = 10;

// // Timing constants
// const unsigned long SENSOR_READ_INTERVAL_MS = 50; // update pressure every 50 ms

// // Variables
// String inputBuffer = "";
// unsigned long lastSensorReadTime = 0;

// void sendString(const String& data) {
//     digitalWrite(RS_DE_RE_SLAVE, HIGH);  
//     delayMicroseconds(50);

//     Serial2.print(data);
//     Serial2.print('\n');
//     Serial2.flush();

//     delayMicroseconds(50);
//     digitalWrite(RS_DE_RE_SLAVE, LOW);
// }

// void setup() {
//     Serial.begin(9600);
//     Serial2.begin(9600);

//     pinMode(RS_DE_RE_SLAVE, OUTPUT);
//     digitalWrite(RS_DE_RE_SLAVE, LOW);  // default to receive

//     String status = SetupCurrentSensor();
//     Serial.println(status);

//     Serial.println("RS485 Slave ready.");
// }

// void loop() {
//     unsigned long currentMillis = millis();

//     // ---- Non-blocking sensor reading ----
//     if (currentMillis - lastSensorReadTime >= SENSOR_READ_INTERVAL_MS) {
//         ReadPressureTransducer();  // updates pressure_readingglobal
//         lastSensorReadTime = currentMillis;
//     }

//     // ---- Handle incoming Serial2 commands ----
//     while (Serial2.available()) {
//         char c = Serial2.read();
//         if (c == '\n') {
//             inputBuffer.trim();
//             if (inputBuffer.length() > 0) {
//                 Serial.print("Received command: ");
//                 Serial.println(inputBuffer);

//                 if (inputBuffer.equalsIgnoreCase("alive")) {
//                     sendString("I am alive");
//                 } else if (inputBuffer.equalsIgnoreCase("PRESS?")) {
//                     // Use pressure_readingglobal if valid, else send <no data>
//                     if (pressure_readingglobal != 0.0) {
//                         sendString(String(pressure_readingglobal, 2));
//                         Serial.println("Sent pressure: " + String(pressure_readingglobal, 2));
//                     } else {
//                         sendString("<no data>");
//                         Serial.println("Sent <no data>");
//                     }
//                 }
//             }
//             inputBuffer = "";
//         } else {
//             inputBuffer += c;
//         }
//     }

//     // ---- Optional: handle Serial monitor input ----
//     while (Serial.available()) {
//         char c = Serial.read();
//         if (c == '\n') {
//             inputBuffer.trim();
//             if (inputBuffer.length() > 0) {
//                 sendString(inputBuffer);
//                 Serial.print("Sent to bus: ");
//                 Serial.println(inputBuffer);
//             }
//             inputBuffer = "";
//         } else {
//             inputBuffer += c;
//         }
//     }
// }



// #include <Arduino.h>
// #include <HardwareSerial.h>
// #include "pressure_functions.h"  // contains pressure_readingglobal

// const int RS_DE_RE_SLAVE = 10;
// const unsigned long SENSOR_READ_INTERVAL_MS = 50; // update sensor every 50 ms

// // Timing & state
// unsigned long lastSensorReadTime = 0;
// String inputBuffer = "";

// // RS485 transmit helper
// void sendString(const String& data) {
//     digitalWrite(RS_DE_RE_SLAVE, HIGH);  // switch to transmit
//     delayMicroseconds(10);

//     Serial2.print(data);
//     Serial2.print('\n');
//     Serial2.flush();

//     delayMicroseconds(10);
//     digitalWrite(RS_DE_RE_SLAVE, LOW);  // back to receive
// }

// void setup() {
//     Serial.begin(9600);
//     Serial2.begin(9600);

//     pinMode(RS_DE_RE_SLAVE, OUTPUT);
//     digitalWrite(RS_DE_RE_SLAVE, LOW); // default receive mode

//     String status = SetupCurrentSensor();  // initialize INA219
//     Serial.println(status);

//     Serial.println("RS485 Slave ready.");
// }

// void loop() {
//     unsigned long currentMillis = millis();

//     // ---- Periodic sensor update (non-blocking) ----
//     if (currentMillis - lastSensorReadTime >= SENSOR_READ_INTERVAL_MS) {
//         ReadPressureTransducer();  // updates pressure_readingglobal
//         lastSensorReadTime = currentMillis;
//     }

//     // ---- Handle incoming Serial2 commands ----
//     while (Serial2.available()) {
//         char c = Serial2.read();
//         inputBuffer += c;

//         if (c == '\n') {  
//             inputBuffer.trim();

//             if (inputBuffer.equalsIgnoreCase("PRESS?")) {
//                 // send pressure or <no data> if zero
//                 if (pressure_readingglobal != 0.0) {
//                     sendString(String(pressure_readingglobal, 2));
//                     Serial.println("Sent pressure: " + String(pressure_readingglobal, 2));
//                 } else {
//                     sendString("<no data>");
//                     Serial.println("Sent <no data>");
//                 }
//             } else if (inputBuffer.equalsIgnoreCase("alive")) {
//                 sendString("I am alive");
//             }

//             inputBuffer = "";  
//         }
//     }

//     // ---- Optional: handle Serial monitor input ----
//     while (Serial.available()) {
//         char c = Serial.read();
//         inputBuffer += c;
//         if (c == '\n') {
//             inputBuffer.trim();
//             if (inputBuffer.length() > 0) {
//                 sendString(inputBuffer);
//                 Serial.println("Sent to bus: " + inputBuffer);
//             }
//             inputBuffer = "";
//         }
//     }
// }

// LATEST WORKING

// #include <Arduino.h>
// #include <HardwareSerial.h>
// #include "pressure_functions.h"

// const int RS_DE_RE_SLAVE = 10;
// unsigned long lastSensorReadTime = 0;
// const unsigned long SENSOR_READ_INTERVAL_MS = 50;

// void sendString(const String& data) {
//     digitalWrite(RS_DE_RE_SLAVE, HIGH);
//     delayMicroseconds(50);
//     Serial2.print(data);
//     Serial2.print('\n');
//     Serial2.flush();
//     delayMicroseconds(50);
//     digitalWrite(RS_DE_RE_SLAVE, LOW);
// }

// void setup() {
//     Serial.begin(9600);
//     Serial2.begin(9600);
//     pinMode(RS_DE_RE_SLAVE, OUTPUT);
//     digitalWrite(RS_DE_RE_SLAVE, LOW);

//     Serial.println(SetupCurrentSensor());
// }

// void loop() {
//     // Update sensor reading every 50 ms
//     if (millis() - lastSensorReadTime >= SENSOR_READ_INTERVAL_MS) {
//         ReadPressureTransducer();  // updates pressure_readingglobal
//         lastSensorReadTime = millis();
//     }

//     // Handle incoming RS485 commands
//     if (Serial2.available()) {
//     String cmd = Serial2.readStringUntil('\n');
//     cmd.trim();

//     if (cmd.equalsIgnoreCase("alive")) {
//         sendString("I am alive");
//        // Serial.println("Sent: I am alive");
//     }
//     else if (cmd.equalsIgnoreCase("PRESS?")) {
//         if (pressure_readingglobal != 0.0) {
//             sendString(String(pressure_readingglobal, 3) + "," + String(current_readingglobal, 3));
//             //sendString();
//            // Serial.println("Sent current: " + String(current_readingglobal, 2));
//         } else {
//             sendString("<no data>");
//            // Serial.println("Sent <no data>");
//         }
//     }
// }
// }


  // #include <Arduino.h>
  // #include <HardwareSerial.h>
  // #include "pressure_functions.h"
  // #include "EC.h"
  // #include  <Servo.h>


  // const int RS_DE_RE_SLAVE = 10;
  // unsigned long lastSensorReadTime = 0;
  // const unsigned long SENSOR_READ_INTERVAL_MS = 50;

  // // Fire/Fill sequence variables
  // int fireSeqState = 0;
  // unsigned long fireStartTime = 0;

  // // RS485 helper
  // void sendString(const String& data) {
  //     digitalWrite(RS_DE_RE_SLAVE, HIGH);
  //     delayMicroseconds(50);
  //     Serial2.print(data);
  //     Serial2.print('\n');
  //     Serial2.flush();
  //     delayMicroseconds(50);
  //     digitalWrite(RS_DE_RE_SLAVE, LOW);
  // }

  // void setup() {
  //     Serial.begin(9600);
  //     Serial2.begin(9600);
  //     pinMode(RS_DE_RE_SLAVE, OUTPUT);
  //     digitalWrite(RS_DE_RE_SLAVE, LOW);

  //     Serial.println(SetupCurrentSensor());
  //     Serial.println("RS485 Slave ready.");
  // }

  // void loop() {
  //     unsigned long currentMillis = millis();

  //     // ---- Periodic sensor reading ----
  //     if (currentMillis - lastSensorReadTime >= SENSOR_READ_INTERVAL_MS) {
  //         ReadPressureTransducer();  // updates globals
  //         lastSensorReadTime = currentMillis;

  //         // Send pressure automatically to master
  //         sendString(String(pressure_readingglobal, 3) + "," + String(current_readingglobal, 3));
  //     }

  //     // ---- Handle incoming RS485 commands ----
  //     while (Serial2.available()) {
  //         String cmd = Serial2.readStringUntil('\n');
  //         cmd.trim();

  //         if (cmd.equalsIgnoreCase("alive")) {
  //             sendString("I am alive");
  //         } 
  //         else if (cmd.equalsIgnoreCase("PRESS?")) {
  //             sendString(String(pressure_readingglobal, 3) + "," + String(current_readingglobal, 3));
  //         } 
  //         else if (cmd.equalsIgnoreCase("FIRE")) {
  //             fireStartTime = currentMillis;
  //             fireSeqState = 0;  // reset fire sequence
  //             sendString("Fire sequence started");
  //         }
  //         else if (cmd.equalsIgnoreCase("FILL")) {
  //             fillSequence();
  //             sendString("Fill sequence executed");
  //         }
  //     }

  //     // ---- Fire sequence non-blocking ----
  //     if (fireSeqState >= 0) {
  //         int countdown = fireSequence(fireStartTime, currentMillis, fireSeqState);
  //         fireSeqState++;  // advance the sequence step-by-step
  //     }
  // }
