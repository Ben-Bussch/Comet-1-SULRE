#pragma once
#include <Arduino.h>

void SetupControl(int PyroPin, int FirePin, int FillSequPin);
void Rest();
int fillSequence(int FillStartTime, int clk_time, int fillSeq);
int fireSequence(int FireStartTime, int clk_time, int FireSeq, int PyroPin);


