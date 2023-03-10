#include <ArduinoJson.h>

// Global variables for communication

/* component readings  */
int com = 0;                      // Represents the communication number for message dropping handling
int joysticks_left_x = 0;         // left analog joystick x value
int joysticks_left_y = 0;         // left analog joystick y value
int joysticks_right_x = 0;        // right analog joystick x value
int joysticks_right_y = 0;        // right analog joystick y value

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

void sendResponse() {
  // Json incoding for the current string, use this url to determinefurute strings
  // https://arduinojson.org/v6/assistant/
  // See arduino-json-form.json. To make changes, paste it into the tool above and add fields.
  // Use 1024 for all numeric values so tool identifies them as such, but leave the portions \
  // of the code below that already have the correct variables substituted in.
  StaticJsonDocument<192> doc;

  doc["COM"] = com++;

  /*-Joysticks-----------------------------------------------------------*/
  
  JsonObject joysticks = doc.createNestedObject("joysticks");
  
  JsonObject joysticks_left = joysticks.createNestedObject("left");
  joysticks_left["x"] = joysticks_left_x;
  joysticks_left["y"] = joysticks_left_y;
  
  JsonObject joysticks_right = joysticks.createNestedObject("right");
  joysticks_right["x"] = joysticks_right_x;
  joysticks_right["y"] = joysticks_right_y;
  
  /*-Actuators-----------------------------------------------------------*/
  
  JsonObject actuators = doc.createNestedObject("actuators");

  JsonObject actuators_1 = actuators.createNestedObject("1");
  actuators_1["pos"] = actuator_1_pos;
  
  JsonObject actuators_1_current_alarm = actuators_1.createNestedObject("current_alarm");
  actuators_1_current_alarm["left"] = actuator_1_alarm_left;
  actuators_1_current_alarm["right"] = actuator_1_alarm_right;

  /*
  JsonObject actuators_2 = actuators.createNestedObject("2");
  actuators_2["pos"] = actuator_2_pos;
  
  JsonObject actuators_2_current_alarm = actuators_2.createNestedObject("current_alarm");
  actuators_2_current_alarm["left"] = actuator_2_alarm_left;
  actuators_2_current_alarm["right"] = actuator_2_alarm_right;
  */

  /*--Write-serial-to-RPi------------------------------------------------*/
  
  size_t bytesWritten = serializeJson(doc, Serial);
  Serial.write('\n');
}

void readSerial() {
  StaticJsonDocument<192> doc;
  if(Serial.available()) {
    String received = Serial.readStringUntil(0);
    DeserializationError error = deserializeJson(doc, received);
    
    if(!error) {
      actuator_1_desired_pos = doc["actuators"]["1"]["move_to"];
      actuator_2_desired_pos = doc["actuators"]["2"]["move_to"];
    } else {
      Serial.println(error.f_str());
    }
  }
}

int Com(int comCNT){
  if (com+1 == comCNT){
    com++;
  }
  else{
    // Implement some sort of error throw here
  }
  return com;
}

//---------------PIN-I/O-----------//
#define LEFT_JOY_X_PIN A0
#define LEFT_JOY_Y_PIN A1 
#define RIGHT_JOY_X_PIN A2
#define RIGHT_JOY_Y_PIN A3

#define ACTUATOR_1_POS_PIN A13
#define ACTUATOR_1_L_ALARM_PIN A14
#define ACTUATOR_1_R_ALARM_PIN A15

#define ACTUATOR_1_EXTEND_PIN 2
#define ACTUATOR_1_RETRACT_PIN 3

#define ACTUATOR_MAX_SPEED 255
#define ACTUATOR_MIN_SPEED 5
#define ACTUATOR_SLOW_DISTANCE 150
#define ACTUATOR_PRECISION 1

void readHardware() {
  joysticks_left_x = analogRead(LEFT_JOY_X_PIN);
  joysticks_left_y = analogRead(LEFT_JOY_Y_PIN);
  
  joysticks_right_x = analogRead(RIGHT_JOY_X_PIN);
  joysticks_right_y = analogRead(RIGHT_JOY_Y_PIN);
  
  actuator_1_pos = analogRead(ACTUATOR_1_POS_PIN);
  actuator_1_alarm_left = analogRead(ACTUATOR_1_L_ALARM_PIN);
  actuator_1_alarm_right = analogRead(ACTUATOR_1_R_ALARM_PIN);

  /*
  actuator_2_pos = analogRead(ACTUATOR_2_POS_PIN);
  actuator_2_alarm_left = analogRead(ACTUATOR_2_L_ALARM_PIN);
  actuator_2_alarm_right = analogRead(ACTUATOR_2_R_ALARM_PIN);
  */
}

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
  
  Serial.begin(9600);    //Raspberry Pi connection
}

void loop() {
  readSerial();
  readHardware();
  sendResponse();
  actuators();
}
