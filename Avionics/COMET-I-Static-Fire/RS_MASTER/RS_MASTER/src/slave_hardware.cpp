// #include <Arduino.h>

// const int RS_RTS = 37;

// void setup() {
//   Serial.begin(9600);
//   Serial2.begin(9600); // Using Hardware Serial 2
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
//     Serial2.write(outgoingData); // Send data to Master via Hardware Serial 2
//     delay(100);
//     digitalWrite(RS_RTS, LOW);
//   }

//   if (Serial2.available()) { 
//     char incomingData = Serial2.read(); 
//     Serial.print("Received: ");
//     Serial.println(incomingData);
//     digitalWrite(LED_BUILTIN, HIGH);
//     delay(100);
//     digitalWrite(LED_BUILTIN, LOW);
//   }
// }