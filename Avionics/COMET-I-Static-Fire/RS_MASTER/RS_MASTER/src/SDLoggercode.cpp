// #include "SDLogger.h"
// #include <SD.h>
// #include <SPI.h>

// static File logFile;
// static String filename = "log.csv";

// void initSDLogger(uint8_t csPin) {
//     if (!SD.begin(csPin)) {
//         Serial.println("SD card initialization failed!");
//     } else {
//         Serial.println("SD card ready.");
//         // Create file and write header if not exists
//         if (!SD.exists(filename.c_str())) {
//             logFile = SD.open(filename.c_str(), FILE_WRITE);
//             if (logFile) {
//                 logFile.println("timestamp,data");
//                 logFile.close();
//             }
//         }
//     }
// }

// void logToCSV(const String& data) {
//     logFile = SD.open(filename.c_str(), FILE_WRITE);
//     if (logFile) {
//         logFile.print(millis());
//         logFile.print(",");
//         logFile.println(data);
//         logFile.close();
//     } else {
//         Serial.println("Failed to open log.csv for writing.");
//     }
// }