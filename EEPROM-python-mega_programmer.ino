#define WE 2
#define OE 23
#define FD 24
#define LD 31
#define FA 32
#define LA 44

void setup() {
    digitalWrite(WE, HIGH);
  digitalWrite(OE, HIGH);
  pinMode(WE, OUTPUT);
  pinMode(OE, OUTPUT);
  digitalWrite(WE, HIGH);
  digitalWrite(OE, HIGH);
  
  for(int pin=FA; pin<=LA; pin++){
    pinMode(pin, OUTPUT);
  }
  Serial.begin(9600);

}

void loop() {
  char mode;
  delay(1);
  Serial.write('p');
  while(!Serial.available()){}
    mode = Serial.read();
    Serial.write(mode);


  while(!Serial.available() && (mode == 'w' || mode == 'r')){}
  if(mode == 'w'){
      byte code[192];
      Serial.readBytes(code, 192);
      for(int i = 0; i < 192; i++){
        writeEeprom(i, code[i]);
        Serial.write(readEeprom(i));
        
      }
  }
  else if(mode == 'r'){
      for(int i = 0; i < 192; i++){
        Serial.write(readEeprom(i));
      }
   
  }

}

void setAddress(int address, bool output){
  for(int pin=FA; pin<=LA; pin++){
    digitalWrite(pin, address & 1);
    address = address >> 1;
  }
 
  digitalWrite(OE, !output);
}


void loadData(byte data){
  for(int pin=FD; pin<=LD; pin++){
    pinMode(pin, OUTPUT);
  }
  for(int pin=FD; pin<=LD; pin++){
    digitalWrite(pin, data & 1);
    
    data = data >> 1;
  }
}

void writeEeprom(int address, byte data){
  setAddress(address, false);
  loadData(data);
  digitalWrite(WE, LOW);
  delayMicroseconds(1);
  digitalWrite(WE, HIGH);
  delay(10);
}


byte readEeprom(int address){
  for(int pin=FD; pin<=LD; pin++){
    pinMode(pin, INPUT);
  }
  setAddress(address, true);
  delayMicroseconds(1);
  byte data;
  for(int i=LD; i>=FD; i--){
    data = (data << 1) + digitalRead(i);
  }
  return data;
}
