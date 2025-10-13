// #include <Arduino.h>

// const int RS_DE_RE = 10;  // DE + RE tied

// void setup() {
//   Serial.begin(9600);       // USB Serial Monitor
//   Serial2.begin(9600);      // RS485 bus on pins 7=RX2, 8=TX2

//   pinMode(RS_DE_RE, OUTPUT);
//   digitalWrite(RS_DE_RE, LOW); // start in receive mode

//   Serial.println("RS485 Master ready...");
// }

// void sendByte(char c) {
//   digitalWrite(RS_DE_RE, HIGH);   // enable transmit
//   delayMicroseconds(10);          // allow MAX485 to settle
//   Serial2.write(c);
//   Serial2.flush();                // wait until UART finishes
//   delayMicroseconds(50);          // guard time
//   digitalWrite(RS_DE_RE, LOW);    // back to receive
// }

// void loop() {
//   // Check if anything typed in Serial Monitor
//   if (Serial.available()) {
//     char msg = Serial.read();
//     Serial.print("Master sending: ");
//     Serial.println(msg);

//     // Send over RS485 using DE/RE control
//     sendByte(msg);
//   }
// }
