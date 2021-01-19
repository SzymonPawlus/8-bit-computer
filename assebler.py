import sys
import re
import math

sys.tracebacklimit = 0

machineCode = [0x00] * 192

commandsOne = ["BCK", "OTA", "ADD", "SUB", "CMP", "HALT", "PUA", "POA", "RET"]
commandsTwo = ["LAI", "LAM", "STA", "LAP", "LBI", "LBM", "JMP", "JMZ", "JMC", "SAP", "JSR", "LSI", "LBP", "STB", "SBP"]

commandsCode = {"BCK": 0x0, "LAI": 0x1, "LAM": 0x2, "STA": 0x3,
                "LAP": 0x4, "LBI": 0x5, "LBM": 0x6, "OTA": 0x7,
                "ADD": 0x8, "SUB": 0x9, "CMP": 0xa, "JMP": 0xb,
                "JMZ": 0xc, "JMC": 0xd, "SAP": 0xe, "HALT": 0xf,
                "PUA": 0x10, "POA": 0x11, "JSR": 0x12, "RET": 0x13,
                "LSI": 0x14, "LBP": 0x15, "STB": 0x16, "SBP": 0x17}


def lineDivide(code):
    return code.split("\n")


def trimComment(line):
    return line.split(";", 1)[0]


def partition(line):
    return line.split()


def syntaxCheck(line, num):
    length = len(line)
    if length == 0:
        return ""
    for command in commandsOne + commandsTwo:
        if length == 1:
            if re.search(command, line[0], re.IGNORECASE):
                return ""
        if length == 2:
            if re.search(command, line[0], re.IGNORECASE) and re.search("^[a-zA-Z0-9-*_]*$", line[1]):
                return ""
    if length == 3:
        if line[0] == "#define" and re.search("^[a-zA-Z0-9-*_]*$", line[1]) and re.search("0[xX][0-9a-fA-F]+", line[2]):
            return ""
        if re.search("DB", line[0], re.IGNORECASE) and re.search("^[a-zA-Z0-9_]*$", line[1]) and re.search(
                "^[a-zA-Z0-9_]*$", line[2]):
            return ""
    if length == 1:
        if re.search("^\.\w+[a-zA-Z0-9_]:", line[0]):
            return ""
    raise ValueError("Syntax not match at line " + str(num))


def bytesCount(line):
    for command in commandsOne:
        if re.search(command, line[0], re.IGNORECASE):
            return 1
    for command in commandsTwo:
        if re.search(command, line[0], re.IGNORECASE):
            return 2
    return 0


def getLabel(line, byte):
    if line[0] == "#define":
        return line[1], int(line[2], 0)
    elif re.search("^\.\w+[a-zA-Z0-9_]:", line[0]):
        return line[0][1:-1], byte
    else:
        return None, None


def printByteArray(array):
    print("Add:  0    1    2    3    4    5    6    7    8    9    a    b    c    d    e    f")
    try:
        for y in range(0, math.ceil(len(array) / 16)):
            print("0x{0:02x}: ".format(y), end="")
            for x in range(0, 16):
                print("0x{0:02x}".format((array[16 * y + x])), end=" ")
            print()
    except:
        return

def wrtieByteArrayToFile(array, file):
    try:
        for y in range(0, math.ceil(len(array) / 16)):
            toPrint = ""
            for x in range(0, 16):
                toPrint += "0x{0:02x}, ".format((array[16 * y + x]))
            file.write(toPrint + "\n")
    except:
        return


# args check
if len(sys.argv) < 3:
    raise ValueError("Too few parameters")

# open file
f = open(sys.argv[1], "r")
code = f.read()
f.close()

# divide code to lines
lines = lineDivide(code)

# delete comments
for x in range(0, len(lines)):
    lines[x] = trimComment(lines[x])

# partition code
for x in range(0, len(lines)):
    lines[x] = partition(lines[x])

# check syntax correctness
for x in range(0, len(lines)):
    error = syntaxCheck(lines[x], x)
    if error != "":
        raise ValueError(error)

# set labels
labels = {}
programBytes = 0
x = 0
for line in lines:
    if len(line) == 0:
        continue
    lineBytes = bytesCount(line)
    if lineBytes > 0:
        programBytes += lineBytes
    else:
        label = getLabel(line, programBytes)
        if label[0] in labels:
            raise ValueError("Repeated label at line " + str(x))
        elif label[0] is not None:
            labels[label[0]] = label[1]
    x += 1
# clear empty lines and labels set
lines = [x for x in lines if x != []]

# change labels to addresses
for x in range(0, len(lines)):
    for command in commandsTwo:
        if re.search(command, lines[x][0], re.IGNORECASE):
            try:
                lines[x][1] = int(lines[x][1], 0)
            except:
                try:
                    lines[x][1] = labels[lines[x][1]]
                except Exception as e:
                    raise ValueError("Parameter error at line " + str(x))
    if re.search("DB", lines[x][0], re.IGNORECASE):
        try:
            lines[x][1] = int(lines[x][1], 0)
        except:
            try:
                lines[x][1] = labels[lines[x][1]]
            except Exception as e:
                raise ValueError("Parameter error at line " + str(x))
        try:
            lines[x][2] = int(lines[x][2], 16)
        except:
            try:
                lines[x][2] = labels[lines[x][2]]
            except Exception as e:
                raise ValueError("Parameter error at line " + str(x))
        machineCode[lines[x][1]] = lines[x][2]

# delete no bytes commands
lines = [x for x in lines if bytesCount(x) != 0]

# change mnemonics to command number
for x in range(0, len(lines)):
    lines[x][0] = commandsCode[lines[x][0].upper()]

# write the list of command numbers
x = 0
for line in lines:
    for word in line:
        machineCode[x] = int(word)
        x += 1

# write to binary file
binFile = open(str(sys.argv[2]) +".bin", "wb")
binFile.write(bytes(machineCode))
binFile.close()

# write to txt file
txtFile = open(str(sys.argv[2]) + ".txt", "w")
wrtieByteArrayToFile(machineCode, txtFile)
txtFile.close()

print()
