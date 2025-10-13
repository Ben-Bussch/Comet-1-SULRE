// #include <Arduino.h>

// const int RS_DE_RE = 37; // DE+RE tied on slave

// void setup() {
//   Serial.begin(9600);      // USB Serial Monitor
//   Serial2.begin(9600);     // RS485 bus (TX2=8, RX2=7)

//   pinMode(RS_DE_RE, OUTPUT);
//   digitalWrite(RS_DE_RE, LOW); // start in receive mode

//   Serial.println("RS485 Slave ready...");
// }

// void loop() {
//   while (Serial2.available()) {
//     int rawByte = Serial2.read(); // read as int to see full 0-255

//     Serial.print("");
//     //Serial.println(rawByte);

//     //Serial.print("Byte check: ");
//     Serial.println((byte)rawByte); // print as character
//     //Serial.println((int)rawByte); // extra blank line for readability
//     //Serial.println((char)rawByte); // print as character

//     Serial.println(); // extra blank line for readability
//   }
// }


// #include <Arduino.h>

// const int RS_DE_RE = 10;  // DE + /RE tied
// const unsigned long SEND_INTERVAL = 1000; // ms between messages

// void setup() {
//   Serial.begin(9600);    // USB monitor
//   Serial2.begin(9600);   // RS485 bus on pins 7=RX2, 8=TX2

//   pinMode(RS_DE_RE, OUTPUT);
//   digitalWrite(RS_DE_RE, LOW); // start in receive mode
//   Serial.println("RS485 Master ready...");
// }

// void sendByte(char c) {
//   digitalWrite(RS_DE_RE, HIGH);   // enable transmit
//   delayMicroseconds(10);          // allow MAX485 to settle
//   Serial2.write(c);
//   Serial2.flush();                // wait for UART to finish
//   delayMicroseconds(50);          // guard time
//   digitalWrite(RS_DE_RE, LOW);    // back to receive
// }

// unsigned long lastSend = 0;

// void loop() {
//   unsigned long now = millis();
//   if (now - lastSend >= SEND_INTERVAL) {
//     lastSend = now;

//     String msg = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789[];,."; // send a test byte
//     Serial.print("Master sending: ");
//     Serial.println(msg);
//     sendByte(msg);
//   }

  // Listen for response from slave
//   if (Serial2.available()) {
//     char c = Serial2.read();
//     Serial.print("Master received: ");
//     Serial.println(c);
 // }
//}