int motor1pin1 = 9;
int motor1pin2 = 10;
// Encoder m1encoder(2, 3);

int motor2pin1 = 6;
int motor2pin2 = 5;
// Encoder m2encoder(11, 15);

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(motor1pin1, OUTPUT);
  pinMode(motor1pin2, OUTPUT);
  pinMode(motor2pin1, OUTPUT);
  pinMode(motor2pin2, OUTPUT);
}

void m1Forward() {
  analogWrite(motor1pin1, 50);
  analogWrite(motor1pin2, 0);
}

void m1Backward() {
  analogWrite(motor1pin1, 0);
  analogWrite(motor1pin2, 50);
}

void m2Forward() {
  analogWrite(motor2pin1, 50);
  analogWrite(motor2pin2, 0);
}

void m2Backward() {
  analogWrite(motor2pin1, 0);
  analogWrite(motor2pin2, 50);
}
void allStop() {
  analogWrite(motor1pin1, 0);
  analogWrite(motor1pin2, 0);
  analogWrite(motor2pin1, 0);
  analogWrite(motor2pin2, 0);
}

void loop() {
  // Serial.println(m1encoder.read());
  // Serial.println(m2encoder.read());
  delay(3000);
  digitalWrite(LED_BUILTIN, HIGH);
  m1Forward();
  m2Forward();
  delay(1000);
  allStop();
  digitalWrite(LED_BUILTIN, LOW);
  delay(1000);
  digitalWrite(LED_BUILTIN, HIGH);
  m1Backward();
  m2Backward();
  delay(1000);
  digitalWrite(LED_BUILTIN, LOW);
  allStop();
}