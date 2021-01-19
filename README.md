# 8-bit-computer IDE

### Requirements:
- npm

## Installation (Developer version only):

### App download

Clone git branch:
`git clone -b IDE --single-branch https://github.com/SzymonPawlus/8-bit-computer.git`

Open terminal in folder with IDE and type:
```
npm install
npm run electron:serve
```

If you setup everything correctly you should see the IDE window

### First setup

From other branches download Compiler (Assembler / HL) and Emulator

From menu bar go `Compiler > Compiler Settings`

Than setup paths to Compiler and Emulator.

If you don't have copy of the computer you may omit `Programmer Location` and `Serial Port` options

### Testing

To test the IDE use one of the examples in examples folder ( **TO CREATE** )

On the beginning of the example they should have description. If emulator output matches it, you configured IDE well.

## Functionalities:

- Highlighting assembler syntax
- Highlighting HL syntax ( **IN PROGRESS** )
- Immidiate compilation and emulation of the program
- Immidiate EEPROM programming
