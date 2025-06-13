void setup() {
  Serial.begin(9600);       // Start serial at 9600 baud
  pinMode(A0, INPUT);       // MQ sensor connected to analog pin A0
}

void loop() {
  int gasValue = analogRead(A0);  // Read the sensor value
  Serial.println(gasValue);       // Send to serial
  delay(200);                     // Adjust sample rate (5Hz = 0.2s interval)
}

