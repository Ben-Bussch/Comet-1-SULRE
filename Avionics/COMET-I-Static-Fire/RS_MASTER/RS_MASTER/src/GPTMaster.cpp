// #include <Arduino.h>
// #include <SoftwareSerial.h>

// const int RS_RX = 7;
// const int RS_TX = 8;
// const int RS_RTS = 10;
// SoftwareSerial RS_Slave(RS_RX, RS_TX);

// void setup() {
//   Serial.begin(9600);
//   RS_Slave.begin(9600);
//   pinMode(RS_RTS, OUTPUT);
//   pinMode(LED_BUILTIN, OUTPUT);
//   digitalWrite(RS_RTS, LOW);
//   while (!Serial) {
//     delay(1);
//   }
//   Serial.println("Starting...");
// }

// void loop() {
//   if (Serial.available()) {
//     char outgoingData = Serial.read(); 
//     digitalWrite(RS_RTS, HIGH);
//     Serial.print("Sending: ");
//     Serial.println(outgoingData);
//     RS_Slave.write(outgoingData); // Send data to Master
//     delay(100);
//     digitalWrite(RS_RTS, LOW);
//   }

//   if (RS_Slave.available()) {
//     char incomingData = RS_Slave.read();
//     Serial.print("Received: ");
//     Serial.println(incomingData);
//     digitalWrite(LED_BUILTIN, HIGH);
//     delay(100);
//     digitalWrite(LED_BUILTIN, LOW);
//   }
// }


// #include <Arduino.h>

// const int RS_DE_RE = 10; // DE+RE tied together

// void setup() {
//   Serial.begin(9600);
//   Serial2.begin(9600);   // Pins 7=RX2, 8=TX2

//   pinMode(RS_DE_RE, OUTPUT);
//   digitalWrite(RS_DE_RE, LOW); // listen by default

//   Serial.println("RS485 Master test start");
// }

// void loop() {
//   digitalWrite(RS_DE_RE, HIGH);   // enable TX
//   delayMicroseconds(50);

//   Serial2.write("A1234567890[];");             // send test byte
//   Serial2.flush();
//   delayMicroseconds(50); // extra guard time
//   digitalWrite(RS_DE_RE, LOW);


//   Serial.println("A1234567890[];");

//   delay(1000);
// }


// #include <Arduino.h>
// #include <HardwareSerial.h>

// const int RS_DE_RE = 10; // DE+RE tied

// void setup() {
//   Serial.begin(9600);    // USB Serial Monitor
//   Serial2.begin(9600);   // RS485 on pins 7=RX2, 8=TX2

//   pinMode(RS_DE_RE, OUTPUT);
//   digitalWrite(RS_DE_RE, LOW); // start in receive

//   pinMode(LED_BUILTIN, OUTPUT);
//   digitalWrite(LED_BUILTIN, HIGH);

//   Serial.println("RS485 Master ready...");
// }

// void sendByte(char c) {
//   digitalWrite(RS_DE_RE, HIGH);   // enable TX
//   delayMicroseconds(100);          // let MAX485 settle
//   Serial2.write(c);
//   Serial2.flush();                // wait until done
//   digitalWrite(RS_DE_RE, LOW);    // back to RX
// }

// void loop() {
//   if (Serial.available()) {
//     char c = Serial.read();
//     Serial.print("Sending: ");
//     Serial.println(c);
//     sendByte(c);
//   }

//   if (Serial2.available()) {
//     char c = Serial2.read();
//     Serial.print("Received: ");
//     Serial.println(c);
//   }
// }


// #include <Arduino.h>
// #include <SoftwareSerial.h>


// // Define RS485 communication pins
// const int RS_RO = 7; // Pin to receive data (RO on MAX485)
// const int RS_DI = 8; // Pin to transmit data (DI on MAX485)
// const int RS_DE_RE = 10; // Pin to enable RS485 transmission (DE/RE on MAX485)

// // Set up SoftwareSerial for RS485 communication
// SoftwareSerial RS_Master(RS_RO, RS_DI);

// void setup() {
//   // Start the RS485 and Serial communication
//   Serial.begin(9600); // For Serial Monitor
//   while (!Serial);
//   RS_Master.begin(9600);  // RS485 baud rate
//   Serial.println("Waiting for data...");
//   pinMode(LED_BUILTIN, OUTPUT);
//   digitalWrite(LED_BUILTIN, HIGH);
//   pinMode(RS_DE_RE, OUTPUT); // Set RS485 DE pin as output
//   digitalWrite(RS_DE_RE, HIGH); // Set to receive mode initially
//   delay(1000);
// }

// void loop() {
//   if (Serial.available()) {
    
//     char incomingData = Serial.read();   
//     Serial.print("Sending: ");
//     Serial.println(incomingData);

//     digitalWrite(RS_DE_RE, HIGH);

    
//     RS_Master.write(incomingData);

//     delay (10);
//     digitalWrite(RS_DE_RE, LOW);
//   }
  
//   if (RS_Master.available()) {
    
//     char receivedData = RS_Master.read();

//     Serial.print("Received: ");
//     Serial.println(receivedData);
//   }
// }