// #include <Arduino.h>
// #include <Pin21Control.h>
// #include <SoftwareSerial.h>

// const int RS_RX = 7;
// const int RS_TX = 8;
// const int RS_RTS = 37;
// const int PIN_21 = 21; // Pin to control

// SoftwareSerial RS_Slave(RS_RX, RS_TX);

// String inputString = "";
// bool stringComplete = false;

// const int servoPins[] = {10, 6, 9}; // Or your actual servo pins

// void writeServo(int pin, int angle) {
//   int pulseWidth = map(angle, 0, 180, 1000, 2000);
//   for (int i = 0; i < 50; i++) {
//     digitalWrite(pin, HIGH);
//     delayMicroseconds(pulseWidth);
//     digitalWrite(pin, LOW);
//     delayMicroseconds(20000 - pulseWidth);
//   }
// }

// void setup() {
//   Serial.begin(9600);
//   RS_Slave.begin(9600);
//   pinMode(RS_RTS, OUTPUT);
//   pinMode(LED_BUILTIN, OUTPUT);
//   pinMode(PIN_21, OUTPUT); // Set pin 21 as output
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

//   while (RS_Slave.available()) {
//     char inChar = (char)RS_Slave.read();
//     if (inChar == '\n' || inChar == '\r') {
//       stringComplete = true;
//     } else {
//       inputString += inChar;
//     }
//   }

//   if (stringComplete) {
//     inputString.trim();
//     Serial.print("Received command: ");
//     Serial.println(inputString);

//     // Handle pin 21 commands
//     handlePin21Command(inputString, PIN_21);

//     // Servo command parsing
//     inputString.toLowerCase();
//     int servoIndex = -1;
//     int angle = -1;

//     if (inputString.startsWith("openservo")) {
//       int pinNum = inputString.substring(9).toInt();
//       for (int i = 0; i < 3; i++) {
//         if (servoPins[i] == pinNum) {
//           servoIndex = i;
//           angle = 180;
//           break;
//         }
//       }
//     } else if (inputString.startsWith("closeservo")) {
//       int pinNum = inputString.substring(10).toInt();
//       for (int i = 0; i < 3; i++) {
//         if (servoPins[i] == pinNum) {
//           servoIndex = i;
//           angle = 0;
//           break;
//         }
//       }
//     }

//     if (servoIndex != -1 && angle != -1) {
//       Serial.print("Moving servo on pin ");
//       Serial.print(servoPins[servoIndex]);
//       Serial.print(" to angle ");
//       Serial.println(angle);
//       writeServo(servoPins[servoIndex], angle);
//     }

//     // Blink LED
//     digitalWrite(LED_BUILTIN, HIGH);
//     delay(100);
//     digitalWrite(LED_BUILTIN, LOW);

//     inputString = "";
//     stringComplete = false;
//   }
// }
