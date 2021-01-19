# Arduino EEPROM programmer

# `EEPROM-mega_programmer.ino`

### Usage:

Pin 2 on Arduino Mega connect to yours EEPROM WEB pin
Pin 23 on Arduino Mega connect to your EEPROM OEB pin
Connect EEPROM CEB pin to ground 

### Adjusting To your EEPROM:

- Program assumes that data bits are connected to the next pins, so adjust 

```
#define FD // First data pin
#define LD // Last data pin
```
- Similarly with address pins:
```
#define FA // First address pin
#define LA // Last address pin
```

### Programing

Connect Arduino to the computer by USB and upload program to the arduino

### Program includes functions for programming:

- Decimal Display EEPROM - `writeDisplay()`
- Microcode Decoder - 'writeCmd()'
- Writing code from `code[]` array - `writeCode()`

# `EEPROM-python-mega_programmer.ino`

Program allows to read and write data to EEPROM using Serial Port Interfacing (for example in python)

[ **NOTE: Program options are adjusted for programming 8-bit computer** ]

### Usage:

- Wait for `p` char on Serial Port
- Send `r` - read or `w` - write to Serial Port
- Wait for character confirmation - You'll recieve the same character as sent one
- If `r` was send previously than sent any character to confim reading
- If `w` was send previously than sent 192 bytes of data to write
- Wait for 192 bytes of read / confirmed data
