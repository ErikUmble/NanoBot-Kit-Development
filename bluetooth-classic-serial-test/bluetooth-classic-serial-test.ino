void setup() {

    digitalWrite(NINA_RESETN, HIGH);
     Serial.begin(115200);
     SerialNina.begin(115200);

     delay(5000); //Delay 5 seconds to allow for user to get ready
}

void loop() {

  int val = 0;
  while(true) {
    int latest = SerialNina.read();
    Serial.print((char)latest);
    Serial.print(" ");
    Serial.println(latest);
    SerialNina.write(val++);
    delay(100);
    val = val % 100;
  }
  
}
