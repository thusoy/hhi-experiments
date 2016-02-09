/* Arduino Code for an EMG SpikerShield to control a TENS device, LED lights, and a gripper */

#include <Servo.h>  //Includes the Gripper Servo Library
Servo ServoGripper; //Declares the Name of the Servo to be ServoGripper -- this is all if you want to control a gripper hand as well

#define NUM_LED 6  //sets the maximum numbers of LEDs
#define MAX_Low 100   //for people with low EMG activity
#define MAX_High 254//for people with high EMG activity
#define Threshold 3 // this sets the light to activate TENS
#define threshold_degrees 10 //Number of steps the Servo will have

int reading[10];
int finalReading;
int StimPin = 3; // TENS Digital 3
int GripPin = 2; //Digital Out that controls Servo Motor Gripper Hand
int MAX = 0;
byte litLeds = 0;
byte multiplier = 1;
byte leds[] = {8, 9, 10, 11, 12, 13};
int aQ1 = 11;
int aQ2 = 13;
int aQ3 = 8;

const int UpdateTime = 200; // (number of milliseconds between updating servo position -- if too low you will burn motor out)
unsigned long OldTime = 0;
int old_degrees = 0;
int new_degrees = 0;

void setup(){
    Serial.begin(9600); //begin serial communications
    ServoGripper.attach(GripPin); //Declare the Servo to be Connected to GripPin
    pinMode(StimPin, OUTPUT); // Set TENS output to StimPin
    for(int i = 0; i < NUM_LED; i++){ //initialize LEDs as outputs
        pinMode(leds[i], OUTPUT);
        pinMode(aQ1, OUTPUT);
    }
    MAX = MAX_High; //This sets the default to people with high EMG activity.
}

void loop(){
    // take ten readings in ~0.02 seconds
    for(int i = 0; i < 10; i++){
        reading[i] = analogRead(A0) * multiplier;
        delay(2);
    }

    // average the ten readings
    for(int i = 0; i < 10; i++){
        finalReading += reading[i];
    }
    finalReading /= 10;

    // write all LEDs low and stim pin low
    for(int j = 0; j < NUM_LED; j++){
        digitalWrite(leds[j], LOW);
        digitalWrite(StimPin, LOW);
    }

    Serial.println(finalReading);
    finalReading = constrain(finalReading, 0, MAX);
    litLeds = map(finalReading, 0, MAX, 0, NUM_LED);

    for (int k = 0; k < litLeds; k++) {
        digitalWrite(leds[k], HIGH); // This turns on the LEDS
        if (k >= Threshold) {
            digitalWrite(StimPin, HIGH); // This turns on the TENS as a function of which LED is lit
        }
    }

    // Translate the analog reading to degrees for the servo (from 165° to 0°).
    new_degrees = map(finalReading, 0 ,MAX, 165, 0);

    if (millis() - OldTime > UpdateTime) {
        if(abs(new_degrees-old_degrees) > threshold_degrees) {
            ServoGripper.write(new_degrees); //Move the servo according to the degrees calculated
        }
        OldTime = millis();
        old_degrees = new_degrees;
    }
}

