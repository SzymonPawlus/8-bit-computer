class Computer:
    def __init__(self):
        self.MEM = [0] * 256
        self.A = 0x00
        self.B = 0x00
        self.Counter = 0
        self.ZF = 0
        self.CF = 0
        self.commands = [self.BCK, self.LAI, self.LAM, self.STA, self.LAP, self.LBI, self.LBM, self.OTA,
                         self.ADD, self.SUB, self.CMP, self.JMP, self.JMZ, self.JMC, self.SAP, self.HALT,
                         self.PUA, self.POA, self.JSR, self.RET, self.LSI, self.LBP, self.STB, self.SBP]
        self.commandsLabels = ["BCK", "LAI", "LAM", "STA", "LAP", "LBI", "LBM", "OTA",
                               "ADD", "SUB", "CMP", "JMP", "JMZ", "JMC", "SAP", "HALT",
                               "PUA", "POA", "JSR", "RET", "LSI", "LBP", "STB", "SBP"]
        self.output = 0
        self.stackPointer = 0

    def clock(self):
        add = self.commands[self.MEM[self.Counter]]()
        self.Counter += add

    def BCK(self):
        self.Counter = 0
        return 0

    def LAI(self):
        self.A = self.MEM[self.Counter + 1]
        return 2

    def LAM(self):
        self.A = self.MEM[self.MEM[self.Counter + 1]]
        return 2

    def STA(self):
        self.MEM[self.MEM[self.Counter + 1]] = self.A
        return 2

    def LAP(self):
        self.A = self.MEM[self.MEM[self.MEM[self.Counter + 1]]]
        return 2

    def LBI(self):
        self.B = self.MEM[self.Counter + 1]
        return 2

    def LBM(self):
        self.B = self.MEM[self.MEM[self.Counter + 1]]
        return 2

    def OTA(self):
        self.output = self.A
        return 1

    def ADD(self):
        self.A += self.B
        self.ZF = self.A == 0
        self.CF = self.A > 255
        self.A = self.A % 256
        return 1

    def SUB(self):
        self.A -= self.B
        self.ZF = self.A == 0
        self.CF = self.A < 0
        self.A = self.A % 256
        return 1

    def CMP(self):
        self.ZF = (self.A + 0 - self.B) == 0
        self.CF = (self.A + 0 - self.B) < 0
        return 1

    def JMP(self):
        self.Counter = self.MEM[self.Counter + 1]
        return 0

    def JMZ(self):
        if self.ZF:
            return self.JMP()
        else:
            return 2

    def JMC(self):
        if self.CF:
            return self.JMP()
        else:
            return 2

    def SAP(self):
        self.MEM[self.MEM[self.MEM[self.Counter + 1]]] = self.A
        return 2

    def HALT(self):
        self.Counter = -1
        return 0

    def PUA(self):
        self.MEM[self.stackPointer] = self.A
        self.stackPointer += 1
        self.stackPointer %= 256
        return 1

    def POA(self):
        self.stackPointer -= 1
        self.stackPointer %= 256
        self.A = self.MEM[self.stackPointer]
        return 1

    def JSR(self):
        self.MEM[self.stackPointer] = self.Counter
        self.Counter = self.MEM[self.Counter + 1]
        self.stackPointer += 1
        self.stackPointer %= 256
        return 0

    def RET(self):
        self.stackPointer -= 1
        self.stackPointer %= 256
        self.Counter = self.MEM[self.stackPointer] + 2
        return 0

    def LSI(self):
        self.stackPointer = self.MEM[self.Counter + 1]
        return 2

    def LBP(self):
        self.B = self.MEM[self.MEM[self.MEM[self.Counter + 1]]]
        return 2

    def STB(self):
        self.MEM[self.MEM[self.Counter + 1]] = self.B
        return 2

    def SBP(self):
        self.MEM[self.MEM[self.MEM[self.Counter + 1]]] = self.B
        return 2
