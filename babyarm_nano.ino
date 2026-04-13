#include <Servo.h>
// ===== Servo Objects =====
Servo servoWrist;
Servo servoShoulder;
Servo servoTurntable;
Servo servoElbow;
Servo servoGripper;

// ===== Pins =====
#define WRIST_PIN 3
#define SHOULDER_PIN 10
#define TT_PIN 6
#define ELBOW_PIN 9
#define GRIPPER_PIN 5

// ===== Positions =====
int wristPos = 90;
int shoulderPos = 90;
int ttPos = 90;
int elbowPos = 90;
int gripperPos = 90;

void moveServo(uint8_t joint, uint8_t angle) {

  angle = constrain(angle, 0, 180);

  switch (joint) {

    case 1:
      wristPos = angle;
      servoWrist.write(wristPos);
      break;

    case 2:
      shoulderPos = angle;
      servoShoulder.write(shoulderPos);
      break;

    case 3:
      elbowPos = angle;
      servoElbow.write(elbowPos);
      break;

    case 4:
      ttPos = angle;
      servoTurntable.write(ttPos);
      break;

    case 5:
      gripperPos = angle;
      servoGripper.write(gripperPos);
      break;
  }
}

void setup() {

  Serial.begin(9600);

  servoWrist.attach(WRIST_PIN);
  servoShoulder.attach(SHOULDER_PIN);
  servoTurntable.attach(TT_PIN);
  servoElbow.attach(ELBOW_PIN);
  servoGripper.attach(GRIPPER_PIN);

  // Home position
  servoWrist.write(wristPos);
  servoShoulder.write(shoulderPos);
  servoTurntable.write(ttPos);
  servoElbow.write(elbowPos);
  servoGripper.write(gripperPos);
}
void loop() {

  static uint8_t buffer[7];
  static uint8_t index = 0;

  while (Serial.available()) {

    uint8_t byteIn = Serial.read();

    if (index == 0 && byteIn != 255) {
      continue;
    }

    buffer[index++] = byteIn;

    if (index == 7) {

      if (buffer[6] == 254) {

        wristPos = constrain(buffer[1],0,180);
        shoulderPos = constrain(buffer[2],0,180);
        elbowPos = constrain(buffer[3],0,180);
        ttPos = constrain(buffer[4],0,180);
        gripperPos = constrain(buffer[5],0,180);

        servoWrist.write(wristPos);
        servoShoulder.write(shoulderPos);
        servoElbow.write(elbowPos);
        servoTurntable.write(ttPos);
        servoGripper.write(gripperPos);
      }

      index = 0;
    }
  }
}