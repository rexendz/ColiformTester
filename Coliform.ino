char rx;
const int probePin = 3;
bool probeIsDetected = false;

void setup() {
  pinMode(3, INPUT);
  Serial.begin(9600);

}

void loop() {
  while(probeIsDetected == false){
    int reading = digitalRead(probePin);
    if(reading == HIGH){
      probeIsDetected = true;
      Serial.println("OK");
    }
     
  }
  while(Serial.available() > 0){
    rx = Serial.read();
    if(rx == '0'){
      float imp1 = 0;
      // do code to read first impedance
      Serial.println(imp1);
    }
    if(rx == '1'){
      float imp2 = 0;
      // do code to read sec impedance
      Serial.println(imp2);
    }
    if(rx == '2'){
      float imp3 = 0;
      // do code to read 3rd impedance
      Serial.println(imp3);
    }
    if(rx == '3'){
      float imp4 = 0;
      // do code to read 4th impedance
      Serial.println(imp4);
    }
    if(rx == '4'){
      float imp5 = 0;
      // do code to read 5th impedance
      Serial.println(imp5);
    }
    if(rx == '5'){
      float imp6 = 0;
      // do code to read 6th impedance
      Serial.println(imp6);
    }
    if(rx == 'R'){
      //reset
    }
  }

}
