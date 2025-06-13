#define RF_PIN 11  // RF transmitter connected to digital pin 11

unsigned long previousGasMillis = 0;
const unsigned long gasInterval = 200;   // sensor reading interval

unsigned long rfSignalStart = 0;
unsigned long rfSignalDuration = 0;
bool rfSignalActive = false;

void setup() {
  pinMode(RF_PIN, OUTPUT);
  pinMode(A0, INPUT);
  digitalWrite(RF_PIN, LOW);
  Serial.begin(9600);
}

void loop() {
  unsigned long currentMillis = millis();

  // 1) Read gas sensor every 200 ms
  if (currentMillis - previousGasMillis >= gasInterval) {
    previousGasMillis = currentMillis;
    int gasValue = analogRead(A0);
    Serial.println(gasValue);
  }

  // 2) Handle serial commands if no RF signal active
  if (!rfSignalActive && Serial.available() > 0) {
    char command = Serial.read();

    if (command == '1') {
      digitalWrite(RF_PIN, HIGH);
      rfSignalStart = currentMillis;
      rfSignalDuration = 200;  // signal ON for 200 ms
      rfSignalActive = true;
      Serial.println("RF signal for '1' sent");
    }
    else if (command == '0') {
      digitalWrite(RF_PIN, HIGH);
      rfSignalStart = currentMillis;
      rfSignalDuration = 1000;  // signal ON for 4000 ms
      rfSignalActive = true;
      Serial.println("RF signal for '0' sent");
    }
    else {
      Serial.println(" Unknown command received");
    }
  }

  // 3) Turn off RF signal after duration
  if (rfSignalActive && (currentMillis - rfSignalStart >= rfSignalDuration)) {
    digitalWrite(RF_PIN, LOW);
    rfSignalActive = false;
  }
}