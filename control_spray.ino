const int SPRAY_PIN = 9;

void setup() {
  pinMode(SPRAY_PIN, OUTPUT);
  Serial.begin(9600);
}

void loop() {

  if (Serial.available()) {
    char c = Serial.read();
    if (c == '1') {
      digitalWrite(SPRAY_PIN, HIGH);  // Spray ON
      delay(100);
      digitalWrite(SPRAY_PIN, LOW); 

    } else if (c == '0') {
      digitalWrite(SPRAY_PIN, HIGH);  // Spray ON
      delay(100);
      digitalWrite(SPRAY_PIN, LOW); 
    }
  }
}
