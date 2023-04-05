/*
Team Rocket 
Aurthor: Marcos De La Osa Cruz & Evan David
Purpose: This sketch controls the arduino mega located within the frame
Its responsible for the following
  - pneumatics system (valves, latches, air compressor)
  - linear actuators (calculating position and writing movements, sending translated positions back to Pi)
  - Motors (calculating position and writing movements, sending translated positions back to Pi)

It uses two way serial communication. Sending positional data to the Pi and recieving move commands form the pi 
 */ 

#include <stdbool.h>
#include <Arduino.h>
#include <ArduinoJson.h>

//---------------PIN-I/O-----------//
#define ACTUATOR_1_POS_PIN A13
#define ACTUATOR_1_L_ALARM_PIN A14
#define ACTUATOR_1_R_ALARM_PIN A15

#define ACTUATOR_1_EXTEND_PIN 2
#define ACTUATOR_1_RETRACT_PIN 3

#define ACTUATOR_MAX_SPEED 255
#define ACTUATOR_MIN_SPEED 5
#define ACTUATOR_SLOW_DISTANCE 150
#define ACTUATOR_PRECISION 1

// pneumatics - not wired officially yet
#define SOLENOID_A 11
#define SOLENOID_B 12
#define SOLENOID_C 13
#define AIR_COMPRESSOR 15
#define RIGHT_LATCH 16
#define LEFT_LATCH 17 
#define PRESSURE_SENSOR A6

#define SEND_DATA_WARNING 8    // set to high (temporarily) to cause incoming data interrupt on the Pi
#define RECIEVE_DATA_WARNING 9  // High when the pi is sending data to us (never used)

//---------------Declarations-----------//
void setUpGPIO();
void updateGPIO();
void sendResponse();

//---------------Globals&Structs-----------//
typedef struct pneumaticsInfo{
  bool A;
  bool B;
  bool C;
  bool Compressor;
  bool rightLatch;
  bool leftLatch;
};

typedef struct actuator{
  int actuator_pos = -1;
  int actuator_alarm_left = -1;
  int actuator_alarm_right = -1;
};

typedef struct Motor {
  int nothingyet;
};

pneumaticsInfo pInfo; // tracks solenoid air compressor, and latch positions
actuator rightAct;    // tracks right actuator movement data
actuator leftAct;     // tracks left actuator movement data


int actuator_1_pos = -1;
int actuator_1_alarm_left = -1;
int actuator_1_alarm_right = -1;

int actuator_2_pos = -1;
int actuator_2_alarm_left = -1;
int actuator_2_alarm_right = -1;

/* component control values */
//int actuator_1_control_mode = SET_POSITION /* SET_POSITION | SET_MOTION*/
int actuator_1_desired_pos = -1;          /* 0 - 1024 */

//int actuator_2_control_mode = SET_POSITION /* SET_POSITION | SET_MOTION*/
int actuator_2_desired_pos = -1;          /* 0 - 1024 */

/* pressure sensor; system pressure -> analog read value between 0 - 1024 */
int pressure_reading = 0; /* default for 1 atm is a reading of ~99*/

//---------------Serial-----------//
void serialSetUp(){
  pinMode(SEND_DATA_WARNING, OUTPUT);
  pinMode(RECIEVE_DATA_WARNING, INPUT);
  Serial.begin(9600);     //Debugging serial Monitor
}

// Will requier changing when we connect the motors
void sendResponse() {
StaticJsonDocument<192> doc;

  doc["_COMMENT"] = "json format sent from the arduino in the frame to the Pi";

  JsonObject Actuators = doc.createNestedObject("Actuators");

  JsonObject Actuators_1 = Actuators.createNestedObject("1");
  Actuators_1["pos"] = 1024;

  JsonObject Actuators_1_current_alarm = Actuators_1.createNestedObject("current_alarm");
  Actuators_1_current_alarm["left"] = 1024;
  Actuators_1_current_alarm["right"] = 1024;

  JsonObject Actuators_2 = Actuators.createNestedObject("2");
  Actuators_2["pos"] = 1024;

  JsonObject Actuators_2_current_alarm = Actuators_2.createNestedObject("current_alarm");
  Actuators_2_current_alarm["left"] = 1024;
  Actuators_2_current_alarm["right"] = 1024;

  size_t bytesWritten = serializeJson(doc, Serial);
  Serial.write('\n');

  // Lets the Pi know wesent a message (Pi interrupts triggered)
  digitalWrite(SEND_DATA_WARNING, HIGH);
  delay(100);
  digitalWrite(SEND_DATA_WARNING, LOW);
  return;
}

void readSerial() {
  StaticJsonDocument<192> doc;
  if(Serial.available()) {
    String received = Serial.readStringUntil(0);
    DeserializationError error = deserializeJson(doc, received);
    
    if(!error) {
      // Need to rework the actuator stuff
      actuator_1_desired_pos = doc["Actuators"]["left"]["move_to"];
      actuator_2_desired_pos = doc["Actuators"]["right"]["move_to"];

      // pInfo update
      pInfo.A = doc["Solenoids"]['OpenA'];
      pInfo.B = doc["Solenoids"]['OpenB'];
      pInfo.C = doc["Solenoids"]['OpenC'];
      pInfo.Compressor = doc["Compressor"]["turnOn"];
      pInfo.leftLatch = doc["Latches"]["OpenLeft"];
      pInfo.rightLatch = doc["Latches"]["OpenRight"];

    } else {
      Serial.println(error.f_str());
    }
  }
}

// not sure what this is supposed to do
void readHardware() {
  actuator_1_pos = analogRead(ACTUATOR_1_POS_PIN);
  actuator_1_alarm_left = analogRead(ACTUATOR_1_L_ALARM_PIN);
  actuator_1_alarm_right = analogRead(ACTUATOR_1_R_ALARM_PIN);

  /*
  actuator_2_pos = analogRead(ACTUATOR_2_POS_PIN);
  actuator_2_alarm_left = analogRead(ACTUATOR_2_L_ALARM_PIN);
  actuator_2_alarm_right = analogRead(ACTUATOR_2_R_ALARM_PIN);
  */

  pressure_reading = analogRead(PRESSURE_SENSOR);
}

//---------------PNEUMATICS-----------//
void setUpPneumatics(){
  pinMode(SOLENOID_A, OUTPUT);
  pinMode(SOLENOID_B, OUTPUT);
  pinMode(SOLENOID_C, OUTPUT);
  pinMode(RIGHT_LATCH, OUTPUT);
  pinMode(LEFT_LATCH, OUTPUT);  
  pinMode(AIR_COMPRESSOR, OUTPUT);
  return;
}

// Update the pneumatics state to reflect the pInfo structure, 
void updatePneumatics(){
  digitalWrite(SOLENOID_A,pInfo.A);
  digitalWrite(SOLENOID_B,pInfo.B);
  digitalWrite(SOLENOID_C,pInfo.C);
  digitalWrite(RIGHT_LATCH,pInfo.rightLatch);
  digitalWrite(LEFT_LATCH,pInfo.leftLatch);
  digitalWrite(AIR_COMPRESSOR,pInfo.Compressor);
  return;
}

// added as a function to streamline code base
int readPressureSensor(){
  pressure_reading = analogRead(PRESSURE_SENSOR);
  return pressure_reading;
}

//---------------ACTUATORS-----------//
int actuatorSpeed(int displacement) {
  double distance = abs(displacement);

  if(displacement < ACTUATOR_SLOW_DISTANCE) {
    double speedRange = ACTUATOR_MAX_SPEED - ACTUATOR_MIN_SPEED;
    double speedBoost = speedRange * distance / ACTUATOR_SLOW_DISTANCE;
    int adjustedSpeed = ACTUATOR_MIN_SPEED + speedBoost;
    return min(adjustedSpeed, ACTUATOR_MAX_SPEED);
  } else {
    return ACTUATOR_MAX_SPEED;
  }
}

void actuators() {
  if(actuator_1_desired_pos < 0 || actuator_1_desired_pos > 1024)
    return;
    
  int actuator_1_error = actuator_1_desired_pos - actuator_1_pos;
  int actuator_1_speed = actuatorSpeed(actuator_1_error);
  
  // position decreases from 1024 to 0 as actuator extends from min to max extension 
  
  if(abs(actuator_1_error) > ACTUATOR_PRECISION) {
    if(actuator_1_error < -ACTUATOR_PRECISION) {
      // negative error indicates actuator must extend
      analogWrite(ACTUATOR_1_EXTEND_PIN, actuator_1_speed);
      analogWrite(ACTUATOR_1_RETRACT_PIN, 0);
    } else if(actuator_1_error > +ACTUATOR_PRECISION) {
      // positive error indicates actuator must retract
      analogWrite(ACTUATOR_1_EXTEND_PIN, 0);
      analogWrite(ACTUATOR_1_RETRACT_PIN, actuator_1_speed);
    }
  } else {
    // |error| < actuator_precision indicates actuator can stop
    analogWrite(ACTUATOR_1_EXTEND_PIN, 0);
    analogWrite(ACTUATOR_1_RETRACT_PIN, 0);
  }
}

void setup() {
  pinMode(ACTUATOR_1_EXTEND_PIN, OUTPUT);
  pinMode(ACTUATOR_1_RETRACT_PIN, OUTPUT);
  serialSetUp();
  setUpPneumatics();
}

void loop() {
  readSerial();
  readHardware();
  sendResponse();
  actuators();
}
