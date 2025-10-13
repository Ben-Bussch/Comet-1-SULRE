// #include <Arduino.h>
// #include <SoftwareSerial.h>

// const int RS_RX = 7;
// const int RS_TX = 8;
// const int RS_RTS = 37;
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