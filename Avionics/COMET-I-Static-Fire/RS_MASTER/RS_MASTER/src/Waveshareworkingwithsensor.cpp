// #include <Arduino.h>
// #include <String.h>
// #include <HardwareSerial.h>
// const int RS_DE_RE = 10;  

// void setup() {
//   Serial.begin(9600);       // Serial Monitor
//   Serial2.begin(9600);      // 7=RX2, 8=TX2

//   pinMode(RS_DE_RE, OUTPUT);
//   digitalWrite(RS_DE_RE, LOW); // start in receive mode

//   Serial.println("RS485 Master ready...");
// }

// void sendByte(char c) {
//   digitalWrite(RS_DE_RE, HIGH);   // enable transmit
//   delayMicroseconds(10);          
//   Serial2.write(c);
//   Serial2.flush();                
//   delayMicroseconds(50);          
//   digitalWrite(RS_DE_RE, LOW);    
// }

// void loop() {
  
//   if (Serial.available()) {
//     String msg = Serial.readStringUntil('\n');
//     msg.trim(); 

//     if (msg.length() > 0) {
//       Serial.print("Master sending: ");
//       Serial.println(msg);

      
//       for (int i = 0; i < msg.length(); i++) {
//         sendByte(msg[i]);
//       }
      
//       sendByte('\n');
//     }
//   }
// }