// #include <Arduino.h>
// #include <String.h>
// #include <HardwareSerial.h>



// const int RS_DE_RE_SLAVE = 10;

// void setup() {
  
//   Serial.begin(9600);

 
//   Serial2.begin(9600);

  
//   pinMode(RS_DE_RE_SLAVE, OUTPUT);

  
//   digitalWrite(RS_DE_RE_SLAVE, LOW);

//   Serial.println("Slave is waiting for commands...");
// }

// void loop() {
  
//   if (Serial2.available()) {
    
//     String receivedMessage = Serial2.readStringUntil('\n');

    
//     receivedMessage.trim();

//    if (receivedMessage.length() > 0) {
//       Serial.print("");
//       Serial.println(receivedMessage);
//     }
//     else {
//       Serial.println("No command recieved");
//     }
//   }
// }


