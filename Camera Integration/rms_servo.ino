#include <Servo.h>
#define COMMAND_RATE 20 //hz

int first_number = 0;
int second_number = 0;
String input_string = "";

Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards
Servo myservo2;

int pos_1 = 0;    // variable to store the servo position
int pos_2 = 0;

void setup() {
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  myservo2.attach(6);
  myservo.write(90);
  myservo2.write(90);
  pos_1 = 90;
  Serial.begin(9600);
  while(!Serial){
   
  }  
}

//void loop() {
 //   String mess;
  //if (Serial.available()>0){
  //  char incoming_char = Serial.read();
   // Serial.println(mess);  
 // }
 
void loop() {
  static unsigned long prev_control_time = 0;  
  if (Serial.available() > 0) {
    char incoming_char = Serial.read();
    if (incoming_char != '\n') {
      input_string += incoming_char;
    } else {
      int comma_index = input_string.indexOf(',');
      if (comma_index != -1) {
        first_number = input_string.substring(0, comma_index).toInt();
        second_number = input_string.substring(comma_index + 1).toInt();

        //Serial.print("Received numbers: ");
        //Serial.print(first_number);
        //Serial.print(" and ");
        //Serial.println(second_number);
      } else {
        //Serial.println("Invalid input. Please enter two numbers separated by a comma (e.g., 12,34):");
      }
      input_string = "";
    }
  if ((millis() - prev_control_time) >= (1000 / COMMAND_RATE))
    {
  //pos_1 = myservo.read();
  pos_2 = myservo2.read(); 
  //Serial.println(pos_1);
  //Serial.println(pos_2);
  if (first_number > pos_1){
    myservo.write(pos_1 + 1);
    pos_1 = pos_1 +1;
  } 
  else {
    myservo.write(pos_1 - 1); 
    pos_1 = pos_1 -1;   
  }

  if (second_number > pos_2) {
    myservo2.write(pos_2 + 1);
  }
  else {
    myservo2.write(pos_2 - 1);
    
  } 
  prev_control_time = millis();
    }
  }
}
   
 
