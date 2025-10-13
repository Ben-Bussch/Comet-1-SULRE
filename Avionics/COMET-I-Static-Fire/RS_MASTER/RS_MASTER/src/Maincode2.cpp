// #include <Arduino.h>
// #include <SoftwareSerial.h>
// #include <SDLogger.h>
// #include <Pin21Control.h>


// const int RS_RO = 7; // Pin to receive data (RO on MAX485)
// const int RS_DI = 8; // Pin to transmit data (DI on MAX485)
// const int RS_DE_RE = 10; // Pin to enable RS485 transmission (DE/RE on MAX485)


// const int servoPins[] = {10, 6, 9};  // Define the pins connected to the servos


// SoftwareSerial RS_Master(RS_RO, RS_DI);

// void writeServo(int pin, int angle) { // Function to write angle to servo
  
//   int pulseWidth = map(angle, 0, 180, 1000, 2000);

  
//   for (int i = 0; i < 50; i++) {
//     digitalWrite(pin, HIGH);             // Set the pin HIGH
//     delayMicroseconds(pulseWidth);       // Wait for the pulse width
//     digitalWrite(pin, LOW);              // Set the pin LOW
//     delayMicroseconds(20000 - pulseWidth);  // Wait for the rest of the 20 ms period
//   }
// }

// String inputString = "";
// bool stringComplete = false;

// void setup() { // Setup function
  
//   Serial.begin(9600); // For Serial Monitor
//   while (!Serial);
//   RS_Master.begin(9600);  // RS485 baud rate
//   Serial.println("Waiting for data...");
//   pinMode(LED_BUILTIN, OUTPUT);
//   digitalWrite(LED_BUILTIN, HIGH);
//   pinMode(RS_DE_RE, OUTPUT); // Set RS485 DE pin as output
//   digitalWrite(RS_DE_RE, HIGH); // Set to receive mode initially
//   delay(1000);

  
//   for (int i = 0; i < 3; i++) {
//     pinMode(servoPins[i], OUTPUT);
//   }
//   inputString.reserve(50);
//  // initSDLogger(4); // Use your actual CS pin
// }

// void loop() { // Main loop
//   // Read serial input as a string
//   while (Serial.available()) {
//     char inChar = (char)Serial.read();
//     if (inChar == '\n' || inChar == '\r') {
//       stringComplete = true;
//     } else {
//       inputString += inChar;
//     }
//   }

//   if (stringComplete) {
//     inputString.trim();
//     Serial.print("Command received: ");
//     Serial.println(inputString);

//     // Parse command: openservo10, closeservo6, pin21high, pin21low, etc.
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

//     // --- Handle pin21high and pin21low commands ---
//     if (inputString == "pin21high" || inputString == "pin21low") {
//       Serial.print("Forwarding command to slave: ");
//       Serial.println(inputString);

//       digitalWrite(RS_DE_RE, HIGH);
//       RS_Master.println(inputString); // Send the command as a string
//       delay(10);
//       digitalWrite(RS_DE_RE, LOW);

//       // Blink LED_BUILTIN
//       digitalWrite(LED_BUILTIN, HIGH);
//       delay(100);
//       digitalWrite(LED_BUILTIN, LOW);
//     }
//     // --- End pin21high/pin21low handling ---

//     if (servoIndex != -1 && angle != -1) {
//       Serial.print("Moving servo on pin ");
//       Serial.print(servoPins[servoIndex]);
//       Serial.print(" to angle ");
//       Serial.println(angle);
//       writeServo(servoPins[servoIndex], angle);

//       digitalWrite(RS_DE_RE, HIGH);
//       RS_Master.print(inputString); // Optionally send the command over RS485
//       delay(10);
//       digitalWrite(RS_DE_RE, LOW);

//       // Blink LED_BUILTIN
//       digitalWrite(LED_BUILTIN, HIGH);
//       delay(100);
//       digitalWrite(LED_BUILTIN, LOW);
//     } else if (servoIndex == -1 && angle == -1 && inputString != "pin21high" && inputString != "pin21low") {
//       Serial.println("Invalid command or pin.");
//     }

//     inputString = "";
//     stringComplete = false;
//   }

//   static String receivedLine = "";
//   while (RS_Master.available()) {
//       char inChar = (char)RS_Master.read();
//       if (inChar == '\n' || inChar == '\r') {
//           if (receivedLine.length() > 0) {
//               Serial.print("Received: ");
//               Serial.println(receivedLine);
//               //logToCSV(receivedLine);
//               receivedLine = "";
//           }
//       } else {
//           receivedLine += inChar;
//       }
//   }
// }
