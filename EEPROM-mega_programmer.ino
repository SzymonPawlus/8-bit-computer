#define WE 2
#define OE 23
#define FD 24
#define LD 31
#define FA 32
#define LA 44

#define HLT 0b0000000100000000  // Halt clock
#define CI  0b0000001000000000  // Program counter in
#define CO  0b0000010000000000  // Program counter out
#define CN  0b0000100000000000  // Count
#define AI  0b0001000000000000  // A reg in
#define AO  0b0010000000000000  // A reg out
#define SU  0b0100000000000000  // Subtract
#define SO  0b1000000000000000  // Sum out
#define BI  0b0000000000000001  // B register in
#define BO  0b0000000000000010  // B register out
#define OI  0b0000000000000100  // Output register in
#define MI  0b0000000000001000  // Memory in
#define MO  0b0000000000010000  // Memory out
#define ADI 0b0000000000100000  // Address register in
#define CMD 0b0000000001000000  // Command register in
#define FI  0b0000000010000000  // Flag register in

#define BCK 0x00
#define LAI 0x01
#define LAM 0x02
#define STA 0x03
#define LAP ((byte)0x04)
#define LBI 0x05
#define LBM 0x06
#define OTA ((byte)0x07)
#define ADD 0x08
#define SUB 0x09
#define CMP 0x0a
#define JMP 0x0b
#define JMZ 0x0c
#define JMC 0x0d
#define SAP 0x0e
#define HALT 0x0f

#define Z0C0 0
#define Z1C0 1
#define Z0C1 2
#define Z1C1 3

uint16_t ucode_template[16][8]= {
  { ADI|CO, CMD|MO|CN,      MO|CI,        0,      0,     0, 0, 0 }, // 0x0 BCK - Go back to 0x00
  { ADI|CO, CMD|MO|CN,     ADI|CO, AI|MO|CN,      0,     0, 0, 0 }, // 0x1 LAI (arg) - Load A register Immediately
  { ADI|CO, CMD|MO|CN,     ADI|CO,ADI|MO|CN,  AI|MO,     0, 0, 0 }, // 0x2 LAM (add) - Load A register from memory
  { ADI|CO, CMD|MO|CN,     ADI|CO,ADI|MO|CN,  AO|MI,     0, 0, 0 }, // 0x3 STA (add) - Store A register to memory
  { ADI|CO, CMD|MO|CN,     ADI|CO,ADI|MO|CN, ADI|MO, AI|MO, 0, 0 }, // 0x4 LAP (add) - Load A register from memory by pointer
  { ADI|CO, CMD|MO|CN,     ADI|CO, BI|MO|CN,      0,     0, 0, 0 }, // 0x5 LBI (arg) - Load B register Immediately
  { ADI|CO, CMD|MO|CN,     ADI|CO,ADI|MO|CN,  BI|MO,     0, 0, 0 }, // 0x6 LBM (add) - Load B register from memory 
  { ADI|CO, CMD|MO|CN,      AO|OI,        0,      0,     0, 0, 0 }, // 0x7 OTA - Load Output register from A register
  { ADI|CO, CMD|MO|CN,   SO|AI|FI,        0,      0,     0, 0, 0 }, // 0x8 ADD - Load A register with A + B
  { ADI|CO, CMD|MO|CN,SU|SO|AI|FI,        0,      0,     0, 0, 0 }, // 0x9 SUB - Load A register with A - B
  { ADI|CO, CMD|MO|CN,      SU|FI,        0,      0,     0, 0, 0 }, // 0xa CMP - Set flags register with difference between A and B
  { ADI|CO, CMD|MO|CN,     ADI|CO,    CI|MO,      0,     0, 0, 0 }, // 0xb JMP (arg) - Set Program counter to (arg) 
  { ADI|CO, CMD|MO|CN,         CN,        0,      0,     0, 0, 0 }, // 0xc JMZ (arg) - Jump if zero
  { ADI|CO, CMD|MO|CN,         CN,        0,      0,     0, 0, 0 }, // 0xd JMC (arg) - Jump if carry
  { ADI|CO, CMD|MO|CN,     ADI|CO,ADI|MO|CN, ADI|MO, MI|AO, 0, 0 }, // 0xe SAP (arg) - Store A register by pointer
  { ADI|CO, CMD|MO|CN,        HLT,        0,      0,     0, 0, 0 }, // 0xf HLT
};



/*byte code[] = {
  LBI, 0,
  LAI, 5,
  OTA,
  LBI, 5,
  ADD,
  LBI, 60,
  CMP,
  JMZ, 0x0f,
  JMP, 0x04,
  OTA,
  HALT, 
}; /* - Counting */

/*
#define a   0x33
#define b   0x34
#define gr  0xc0
#define sm  0xc1
#define sum 0xc2
#define j   0xc3

byte code[] = {
  LAM, b, // 0x00
  LBM, a, // 0x02
  CMP, // 0x04
  JMC, 0x09, // 0x05
  JMP, 0x12, // 0x07
  STA, gr, // 0x09
  LAM, a,//0x0b
  STA, sm, // 0x0d
  JMP, 0x17, // 0x0f
  STA, sm, // 0x11
  LAM, a, // 0x13
  STA, gr, // 0x15
  LAI, 0, // 23 0x17
  STA, sum, // 0x19
  LAM, sm, // 0x1b
  STA, j, // 0x1d
  LAM, sum, // 0x1f
  LBM, gr, // 0x22 ***
  ADD, // 0x24
  OTA, // 0x25
  STA, sum, // 0x26
  LAM, j, // 0x28
  LBI, 1, // 0x2a
  SUB, // 0x2c
  STA, j,
  JMZ, 0x32, // 0x2d
  JMP, 0x1f, // 0x2f
  HALT, // 47 0x31
  2, 100,
  
}; /* - Multiplying*/

#define swap 0xc0

/*byte code[] = {
  LAI, 0,
  STA, swap,
  LAI, 1,
  LBI, 0,
  STA, swap,
  ADD,
  JMC, 0x20,
  OTA,
  LBM, swap,
  JMP, 0x08,
  BCK,
};/* - Fibbonaci */

byte code[] = {
0x01, 0x02, 0x03, 0xc5, 0x01, 0x00, 0x03, 0xc2, 0x03, 0xc3, 0x01, 0xd0, 0x03, 0xc0, 0x01, 0xe0, 
0x03, 0xc1, 0x01, 0x01, 0x03, 0xc4, 0x02, 0xc2, 0x03, 0xc3, 0x02, 0xc3, 0x05, 0x00, 0x0a, 0x0c, 
0x4a, 0x04, 0xc0, 0x03, 0xc6, 0x04, 0xc1, 0x06, 0xc6, 0x0a, 0x0c, 0x2e, 0x0b, 0x32, 0x01, 0x00, 
0x03, 0xc4, 0x05, 0x01, 0x04, 0xc1, 0x08, 0x0e, 0xc1, 0x02, 0xc3, 0x09, 0x03, 0xc3, 0x02, 0xc0, 
0x08, 0x03, 0xc0, 0x02, 0xc1, 0x08, 0x03, 0xc1, 0x0b, 0x1a, 0x02, 0xc4, 0x05, 0x01, 0x0a, 0x0c, 
0x53, 0x0b, 0x6f, 0x02, 0xc5, 0x07, 0x05, 0xf7, 0x08, 0x0d, 0x6f, 0x05, 0x01, 0x02, 0xc0, 0x08, 
0x03, 0xc0, 0x02, 0xc1, 0x08, 0x03, 0xc1, 0x01, 0x01, 0x0e, 0xc1, 0x02, 0xc5, 0x0e, 0xc0, 0x05, 
0x01, 0x02, 0xc5, 0x08, 0x0d, 0x7a, 0x03, 0xc5, 0x0b, 0x0a, 0x0f, 0x00, 0x00, 0x00, 0x00, 0x00, 
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 

}; /* - Fibbonaci generated */


uint16_t ucode[4][16][8];

void initUcode(){
  // ZF = 0, CF = 0
  memcpy(ucode[Z0C0], ucode_template, sizeof(ucode_template));
  // ZF = 1, CF = 0
  memcpy(ucode[Z1C0], ucode_template, sizeof(ucode_template));
  ucode[Z1C0][JMZ][2] = ADI|CO;
  ucode[Z1C0][JMZ][3] = CI|MO;
  // ZF = 0, CF = 1
  memcpy(ucode[Z0C1], ucode_template, sizeof(ucode_template));
  ucode[Z0C1][JMC][2] = ADI|CO;
  ucode[Z0C1][JMC][3] = CI|MO;
  // ZF = 1, CF = 1
  memcpy(ucode[Z1C1], ucode_template, sizeof(ucode_template));
  ucode[Z1C1][JMZ][2] = ADI|CO;
  ucode[Z1C1][JMZ][3] = CI|MO;
  ucode[Z1C1][JMC][2] = ADI|CO;
  ucode[Z1C1][JMC][3] = CI|MO;
 
}






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
  //writeDisplay();
  //writeCmd();
  //writeCode();
  readAll(192);
  
 
}




void readAll(int length){
  Serial.println("Reading EEPROM: ");
  Serial.println("Ad:  0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f");
  for(int i=0, k=0; i<length; i++){
    if(i%16==0){
      char bufs[4];
      sprintf(bufs, "%02x: ", k);
      k++;
      Serial.print(bufs);      
    }
    char buf[3];
    sprintf(buf,"%02x ",readEeprom(i));
    Serial.print(buf);
    if(i % 16 == 15){
      Serial.println("");
    }
  }
}

void erase(){
  Serial.print("Erasing EEPROM");
  for(int address = 0; address < 256; address++){
    writeEeprom(address, 0x00);
    if(address%64 == 0){
      Serial.print(".");
    }
  }
  Serial.println();
}

void writeCode(){
  erase();
  Serial.print("Writing code to EEPROM");
  for(int address = 0; address < sizeof(code); address++){
    writeEeprom(address, code[address]);
    if(address%64 == 0){
      Serial.print(".");
    }
  }

  Serial.println("Code saved to EEPROM!");
}

void writeCmd(){
  initUcode();
  Serial.print("Programming EEPROM");
  // Program the 8 high-order bits of microcode into the first 128 bytes of EEPROM
  for (int address = 0; address < 1024; address += 1) {
    int flags       = (address & 0b1100000000) >> 8;
    int bs          = (address & 0b0010000000) >> 7;
    int instruction = (address & 0b0001111000) >> 3;
    int step        = (address & 0b0000000111);
    if(bs){
      writeEeprom(address, ucode[flags][instruction][step]);
    }else{
      writeEeprom(address, ucode[flags][instruction][step] >> 8);
    }
    if (address % 64 == 0) {
      Serial.print(".");
    }
  }
  Serial.println(" done");


  // Read and print out the contents of the EERPROM
  Serial.println("Reading EEPROM");
}

void writeDisplay(){
  byte digits[] = {0x03, 0x9f, 0x25, 0x0d, 0x99, 0x49, 0x41, 0x1f, 0x01, 0x09};
  
  Serial.println("Programming ones place");
  for (int value = 0; value <= 255; value += 1) {
    writeEeprom(value, digits[value % 10]);
  }
  Serial.println("Programming tens place");
  for (int value = 0; value <= 255; value += 1) {
    writeEeprom(value + 256, digits[(value / 10) % 10]);
  }
  Serial.println("Programming hundreds place");
  for (int value = 0; value <= 255; value += 1) {
    writeEeprom(value + 512, digits[(value / 100) % 10]);
  }
  Serial.println("Programming sign");
  for (int value = 0; value <= 255; value += 1) {
    writeEeprom(value + 768, 0xff);
  }
}

void loop() {
 
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
