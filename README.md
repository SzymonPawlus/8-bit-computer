# 8-bit-computer Emulator

### Requirements:
- python 3

### Usage:
In terminal / command promt opened in folder with emulator:
```
python3 main.py (arg1)
```
`(arg1)` - `.bin` file with code f.e. from Assembler.py

In emulator:
- if you want to execute one command only click `Tick`
- if you want to enable clock tick `Start` checkbox and adjust speed on slider

You can track all the variables on the screen

### Flags:
- Zero Flag is set when the result of the addition/subtraction was zero
- Carry Flag is set when additon exceeds 255 or on subtraction when A register value was smaller(**TO CHANGE**) than B register value

