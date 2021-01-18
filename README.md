# 8-bit Assebmly

# Commands

## Basic Set (Physical and Emulator):
- `BCK` - Set program counter to 0
- `LAI (arg)` - Set A register to value (arg)
- `LAM (arg)` - Set A register to value in memory at address (arg)
- `STA (arg)` - Store A register value at memory address (arg)
- `LAP (arg)` - Set A register to value at address pointed by memory value at address (arg)
- `LBI (arg)` - Set B register to value (arg)
- `LBM (arg)` - Set B register to value in memory at address (arg)
- `OTA` - Set Output register to value in A register
- `ADD` - Set A register to sum of values in A and B register [Set Flags]
- `SUB` - Set A register to difference of values in A and B register [Set Flags]
- `CMP` - Set flags like `SUB` [Set Flags]
- `JMP (arg)` - Set Program Counter to value (arg)
- `JMZ (arg)` - Set Program Counter to value (arg) if Zero Flag is set
- `JMC (arg)` - Set Program Counter to value (arg) if Carry Flag is set
- `SAP (arg)` - Store A register value to address pointed by memory value at address (arg)
- `HALT` - Halt the clock

## Extended Set (Emulator only):
- `PUA` - Store A register value to memory address pointed by Stack Pointer and increment Stack Pointer
- `POA` - Decrement Stack Pointer and set A register value to value in memory address pointed by Stack Pointer
- `JSR (arg)` - Store current Program counter value to memory address pointed by Stack Pointer, increment Stack Pointer and set Program Counter value to (arg)
- `RET` - Decrement Stack Pointer and set Program Couter value to value in memory address pointed by Stack Pointer and adds 2 to it
- `LSI (arg)` - Set Stack Pointer value to (arg)
- `LBP (arg)` - Set B register to value at address pointed by memory value at address (arg)
- `STB (arg)` - Store B register value at memory address (arg)
- `SBP (arg)` - Store B register value to address pointed by memory value at address (arg)

# Syntax

- ### `#define` directive
Syntax: 

`#define (arg1) 0x(arg2)`

Explanation:

In code you can use `(arg1)` instead of hex number `0x(arg2)`

Example:

`#define foo 0xc0` - Sets first's RAM cell name to foo

- ###  `.label:` directive:
Syntax:
```
; code
.(arg):
; code
JMP (arg)
```

Explanation:
Marks place in code as `(arg)` so you can make a jump to it

Example:

```
.loop:
JMP loop ; This is infinitive loop
```

- ### `DB` directive:
Syntax:
`DB (add) (byte)`

Explanation:
Store `(byte)` value to `(add)` address in ROM

Example:
`DB 0xbf 0xc0` - Store value `0xc0` - `192` to memory address `0xbf`

- ### Comments:
Syntax:
`(cmd) ; foo comment`

Explanation:
This is description of part of the code / programmer comment

Example:
`LSI 0xf0 ; Intialized Stack Pointer value to address 0xf0`
