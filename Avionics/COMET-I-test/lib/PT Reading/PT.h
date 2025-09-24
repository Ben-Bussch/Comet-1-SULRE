#pragma once
#include <Arduino.h>

String SetupCurrentSensor();
float CurrentToPressure(float current, float intercept, float grad);
float ReadPressureTransducer();