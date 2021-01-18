import serial
import numpy as np
import sys

if len(sys.argv) < 3:
    raise ValueError("Not enough positional arguments")

Bytes = np.fromfile(sys.argv[1], "uint8")

ser = serial.Serial(
    port=sys.argv[2],
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1,
    xonxoff=False,
    rtscts=False,
    dsrdtr=False,
    writeTimeout=2)
ser.close()
ser.open()
print("Preapred WRITE" if ser.read(1) == b'p' else "Something may went wrong")
ser.write('w'.encode())
print("Correct WRITE command sent" if ser.read(1) == b'w' else "Something may went wrong")
ser.write(bytearray(Bytes))
data = ser.readline(192)
print("Program saved correct" if data == bytes(Bytes) else "Program corrupted")

print("Preapred READ" if ser.read(1) == b'p' else "Something may went wrong")
ser.write('r'.encode())
print("Correct READ command sent" if ser.read(1) == b'r' else "Something may went wrong")
ser.write('t'.encode())
data = ser.readline(192)
print("Program saving confirmed" if data == bytes(Bytes) else "Program corrupted")
ser.close()
