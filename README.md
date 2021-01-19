# EEPROM Programmer - Python Interfacing

Program allows to write a 192 bytes long `.bin` file to the EEPROM

[ **Require Software from branch Arduino_Controller on Arduino Mega** ]

### Requirements:
- python 3

### Usage:

In terminal / command promt opened in folder with programmer:
```
python3 main.py (arg1) (arg2)
```

`(arg1)` - Path to the source `.bin` file

`(arg2)` - Serial Port name for Arduino Mega e. `COM2` (Windows), `/dev/ttyUSB0` (Linux)
