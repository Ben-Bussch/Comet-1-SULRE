// #include <Arduino.h>


// const int RS_DE_RE_SLAVE = 10;

// void setup() {
//   Serial.begin(9600);    
//   Serial2.begin(9600);   

//   pinMode(RS_DE_RE_SLAVE, OUTPUT);
//   digitalWrite(RS_DE_RE_SLAVE, LOW); 

//   Serial.println("RS485 Slave ready. Type into Serial Monitor to send to bus.");
// }


// void sendString(const String& data) {
//   digitalWrite(RS_DE_RE_SLAVE, HIGH);   
//   delayMicroseconds(10);                
//   Serial2.print(data);                  
//   Serial2.print('\n');                  
//   Serial2.flush();
//   delayMicroseconds(10);
//   digitalWrite(RS_DE_RE_SLAVE, LOW);    
// }

// void loop() {

//   if (Serial.available()) {
//     String msg = Serial.readStringUntil('\n');
//     msg.trim();
//     if (msg.length() > 0) {
//       sendString(msg);
//       Serial.print("Sent to bus: ");
//       Serial.println(msg);
//     }
//   }

  
//   if (Serial2.available()) {
//     String cmd = Serial2.readStringUntil('\n');
//     cmd.trim();
//     Serial.print("Received from bus: ");
//     Serial.println(cmd);

    
//     if (cmd.equalsIgnoreCase("alive")) {
//       sendString("I am alive");
//       Serial.println("Responded with 'I am alive'");
//     } else if (cmd.equalsIgnoreCase("PRESS?")) {
//       sendString("pressure sensor not connected");
//       Serial.println("Responded with 'pressure sensor not connected'");
//     }
//   }
// }
