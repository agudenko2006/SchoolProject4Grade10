void setup() {
  Serial.begin(9600);
  Serial.println("Format is 'cp' where c is command and p is pin");
  Serial.print("Refference:\n\
commands:\n\
* i initializes specified pin as INPUT_PULLUP\n\
* o initializes specified pin as OUTPUT\n\
* + turns it on\n\
* - turns it off\n\
* ? reads the input as digital\n\
* 0-9 PWM");
}

void loop() {
  while(Serial.available() > 0){
    char cmd = Serial.read();
    if(cmd == '\n') { break; }
    int pin = Serial.parseInt();

    switch(cmd) {
      case 'i': pinMode(pin, INPUT_PULLUP); break;
      case 'p': pinMode(pin, OUTPUT); break;
      case 'o': pinMode(pin, OUTPUT); break;
      case '+': digitalWrite(pin, 1); break;
      case '-': digitalWrite(pin, 0); break;
      case '?': Serial.println(digitalRead(pin)); break;
      case 'a': Serial.println(analogRead(pin)); break;
      default: analogWrite(pin, 255/9*(cmd-'0')); break;
    }
  }
}
