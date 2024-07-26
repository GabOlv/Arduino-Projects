#include <Servo.h>

Servo micro_servo;

int pos = 0;

// Define Trigger, Echo and Servo pins of the Ultrasonic Sensor
const int trigPin = 10;
const int echoPin = 11;
const int ServoPin = 12;

float duration, distance;

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.begin(9600);
  micro_servo.attach(ServoPin); // Define the pin to which the servo motor is attached
}

void loop() {
  for (pos = 15; pos <= 165; pos++) {
    micro_servo.write(pos);
    delay(25); // Pequeno delay para permitir que o servo alcance a posição
    read_ultrasonic_distance(pos);
  }
  for (pos = 165; pos >= 15; pos--) {
    micro_servo.write(pos);
    delay(25); // Pequeno delay para permitir que o servo alcance a posição
    read_ultrasonic_distance(pos);
  }
  delay(10);
}

void read_ultrasonic_distance(int angle) {
  long sum = 0;
  const int numReadings = 5; // Número de leituras para média

  for (int i = 0; i < numReadings; i++) {
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);

    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);

    duration = pulseIn(echoPin, HIGH);
    distance = duration * 0.034 / 2;

    sum += distance;
    delay(10); // Pequeno delay entre leituras
  }

  distance = sum / numReadings; // Calcula a média das leituras

  Serial.print(angle);
  Serial.print(",");
  Serial.println(distance);
}
