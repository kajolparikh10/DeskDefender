//Define Pins
const int btnHappy = 32; //connect to blue
const int btnStressed = 2;
const int btnTired = 12;
const int trigPin = 17;
const int echoPin = 35;

// 2. Hardware States
const int distanceThreshold = 5; //cm (max distance that means phone is ON the robot)
bool isPhoneOn = false;          // Tracks the current state of the phone

void setup() {
  //Python backend
  Serial.begin(115200);
  
  //Setup buttons using internal pull-up resistors
  pinMode(btnHappy, INPUT_PULLUP);
  pinMode(btnStressed, INPUT_PULLUP);
  pinMode(btnTired, INPUT_PULLUP);
  
  //Setup Ultrasonic Sensor
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  
  Serial.println("DeskDefender Hardware Initialized.");
}

void loop() {
  //READ THE MOOD BUTTONS
  //Buttons read low when pressed because they are wired to ground
  if (digitalRead(btnHappy) == LOW) {
    Serial.println("MOOD:Happy");
    delay(500); //Debounce to prevent double-clicking
  }
  else if (digitalRead(btnStressed) == LOW) {
    Serial.println("MOOD:Stressed");
    delay(500);
  }
  else if (digitalRead(btnTired) == LOW) {
    Serial.println("MOOD:Tired");
    delay(500);
  }

  //READ THE ULTRASONIC SENSOR
  //Send a 10 microsecond ping
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  //Read the echo return time
  long duration = pulseIn(echoPin, HIGH);
  
  //Calculate distance in centimeters
  int distance = duration * 0.034 / 2;

  //TRIGGER THE PYTHON BACKEND
  //If the distance is between 0.1cm and 5cm, the phone is ON the robot
  if (distance >= 0.1 && distance <= distanceThreshold) {
    if (!isPhoneOn) { //Only trigger if it wasn't already on
      isPhoneOn = true;
      Serial.println("PHONE:ON");
      delay(500); // Prevent sensor bouncing
    }
  } 
  //If the distance is greater than 5cm, the phone was REMOVED
  else if (distance > distanceThreshold) {
    if (isPhoneOn) { //Only trigger if it was previously on
      isPhoneOn = false;
      Serial.println("PHONE:OFF");
      delay(500); //Prevent sensor bouncing
    }
  }

  delay(50); //Small delay to keep the loop stable
}
