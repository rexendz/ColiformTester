#include <PWM.h>
#define pwmPin 3

int32_t frequency1 = 100;
int32_t frequency2 = 2000;
int32_t frequency3 = 5000;
int32_t frequency4 = 10000;
int32_t frequency5 = 30000;
int32_t frequency6= 60000;
unsigned long timer = 0;


void setup() {
  pinMode(2, OUTPUT);
  digitalWrite(2, HIGH);
  
  pinMode(A5, INPUT);
  
  for(int i = 4; i<=9;i++){
    pinMode(i, OUTPUT);
    digitalWrite(i, HIGH);
  }
  
  InitTimersSafe();
  Serial.begin(9600);
  for(int i = 0; i < 10; i++)
    Serial.write('\n');
  analogReference(INTERNAL);
  Serial.println("Relay 1");
  timer = millis();
}

double pwmOut = 127.4;
int reading = 0;
int phase = 1;
bool frequencySet = false;

void loop() {
  if(!frequencySet) {
    SetPinFrequencySafe(pwmPin, phase);
    frequencySet = true;
  }
  relayOn(phase);
  if((millis() - timer) >= 60000) {
    phase++;
    frequencySet = false;
    resetRelays();
    timer = millis();
    Serial.print("RELAY ");
    Serial.println(phase);
  }

  pwmWrite(pwmPin, pwmOut);
  reading = analogRead(A5);
  Serial.print("Reading: ");
  Serial.println(reading);
}

void setFrequency(int frequency) {
  switch(frequency) {
    case 1:
      SetPinFrequencySafe(pwmPin, frequency1);
      break;
    case 2:
      SetPinFrequencySafe(pwmPin, frequency2);
      break;
    case 3:
      SetPinFrequencySafe(pwmPin, frequency3);
      break;
    case 4:
      SetPinFrequencySafe(pwmPin, frequency4);
      break;
    case 5:
      SetPinFrequencySafe(pwmPin, frequency5);
      break;
    case 6:
      SetPinFrequencySafe(pwmPin, frequency6);
      break;
  }
}

void resetRelays() {
  for(int i = 4; i <= 9; i++)
    digitalWrite(i, HIGH);
}

void relayOn(int relay) {
  switch(relay) {
    case 1:
    digitalWrite(4, LOW);
    break;
    case 2:
    digitalWrite(5, LOW);
    break;
    case 3:
    digitalWrite(6, LOW);
    break;
    case 4:
    digitalWrite(7, LOW);
    break;
    case 5:
    digitalWrite(8, LOW);
    break;
    case 6:
    digitalWrite(9, LOW);
    break;
  }
}

void relayOff(int relay) {
  switch(relay) {
    case 1:
    digitalWrite(4, HIGH);
    break;
    case 2:
    digitalWrite(5, HIGH);
    break;
    case 3:
    digitalWrite(6, HIGH);
    break;
    case 4:
    digitalWrite(7, HIGH);
    break;
    case 5:
    digitalWrite(8, HIGH);
    break;
    case 6:
    digitalWrite(9, HIGH);
    break;
  }
}
