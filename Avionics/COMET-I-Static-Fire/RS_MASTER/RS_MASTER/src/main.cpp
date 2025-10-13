// #include <Arduino.h>
// #include <SoftwareSerial.h>


// // Define RS485 communication pins
// const int RS_RO = 8; // Pin to receive data (RO on MAX485)
// const int RS_DI = 7; // Pin to transmit data (DI on MAX485)
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
//   pinMode(RS_DI, OUTPUT); // Set RS485 DE pin as output
//   digitalWrite(RS_DE_RE, HIGH); // Set to receive mode initially
//   pinMode(RS_DE_RE, HIGH);
//   delay(1000);
// }

// void loop() {
//   if (Serial.available()) {

//     char incomingData = Serial.read();
//     Serial.print("Sending: ");
//     Serial.println(incomingData);
    
//     digitalWrite(RS_DI, HIGH);


//     RS_Master.write(incomingData);

//     delay (10);
//     digitalWrite(RS_DI, LOW);
//   }

//   if (RS_Master.available()) {

//     char receivedData = RS_Master.read();

//     Serial.print("Received: ");
//     Serial.println(receivedData);
  
//   }
// }
