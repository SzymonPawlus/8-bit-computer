import re

from lexer import Lexer, Scope, Command, Line


def getBetweenBrackets(text):
    return re.search(r'\((.*?)\)', text).group(1)


class Condition:
    ops = ["==", "!=", ">", "<", ">=", "<="]

    def __init__(self, text):
        self.text = text
        self.value1 = ""
        self.operator = ""
        self.value2 = ""
        self.value1t = ""
        self.value2t = ""
        self.parseCondition()

    def parseCondition(self):
        opFound = [op for op in self.ops if op in self.text]
        if len(opFound) == 1:
            op = opFound[0]
            location = self.text.find(op)
            self.value1 = self.text[0:location - 1].strip()
            self.operator = op
            self.value2 = self.text[location + len(op):].strip()
            self.value1t = "i" if checkIfParsable(self.value1) else "s"
            self.value2t = "i" if checkIfParsable(self.value2) else "s"

        else:
            raise ValueError("Wrong condition parsing")


def checkIfParsable(x):
    try:
        y = int(x)
        y = y + 1
        return True
    except:
        return False


class Compiler:
    def __init__(self):
        f = open("another.txt", "r")
        self.code = f.read()
        f.close()
        self.directives = ""
        self.assembly = ""
        self.currentRAM = 0xc0
        self.lexer = Lexer(self.code)
        self.cmds = self.lexer.lex()
        self.directives += "#define swap {0}\n".format(str(hex(self.currentRAM)))
        self.currentRAM += 1
        self.directives += "#define return {0}\n".format(str(hex(self.currentRAM)))
        self.currentRAM += 1
        self.ifs = 0
        self.whiles = 0
        self.functions = 0
        self.isFunction = False
        self.writeAssembly(self.cmds, "")
        if self.functions > 0:
            self.directives += "#define bsp   0xf0 \n#define *sp   0xdf \n#define stack 0xe0\n"
            self.assembly = "LSI bsp \nLAI stack \nSTA *sp \n" + self.assembly
            self.assembly += ".pusha:\nPUA\nLAM *sp\nLBI 1\nADD\nSTA *sp\nPOA\nSAP *sp\nRET\n.popa:\nLAP *sp\nPUA\nLAM *sp\nLBI 1\nSUB\nSTA *sp\nPOA\nRET"
        f = open("code.txt", "w")
        f.write(self.directives + self.assembly)
        f.close()

    def writeAssembly(self, cmds, funcParam):
        for cmd in cmds:
            if isinstance(cmd, Command):
                self.writeVar(cmd, funcParam)
            if isinstance(cmd, Scope):
                if cmd.keyword == "if":
                    cmd.param = getBetweenBrackets(cmd.param)
                    condition = Condition(cmd.param)
                    num = self.ifs
                    self.ifs += 1
                    self.writeCondition(condition, "if" + str(num) + "code", "if" + str(num) + "end", funcParam)
                    self.assembly += ".if" + str(num) + "code:\n"
                    self.writeAssembly(cmd.commands, funcParam)
                    self.assembly += ".if" + str(num) + "end:\n"
                    continue
                if cmd.keyword == "while":
                    cmd.param = getBetweenBrackets(cmd.param)
                    condition = Condition(cmd.param)
                    num = self.whiles
                    self.assembly += ".while" + str(num) + ":\n"
                    self.writeCondition(condition, "while" + str(num) + "code", "while" + str(self.whiles) + "end", funcParam)
                    self.assembly += ".while" + str(num) + "code:\n"
                    self.writeAssembly(cmd.commands, funcParam)
                    self.assembly += "JMP " + "while" + str(num) + "\n"
                    self.assembly += ".while" + str(num) + "end:\n"
                    self.whiles += 1
                    continue
                if cmd.keyword == "func":
                    firstPar = cmd.param.find("(")
                    funcName = cmd.param[0:firstPar]
                    param = cmd.param.replace(funcName, "").strip()
                    param = getBetweenBrackets(param)
                    self.assembly += "." + funcName + ":\n"
                    self.writeAssembly(cmd.commands, param)
                    self.functions += 1
                    continue
                self.writeAssembly(cmd.commands, "")

    def writeCondition(self, condition, codeLabel, endLabel, funcParam):
        if condition.value1 == funcParam:
            self.assembly += "LAP " + "*sp" + "\n"
        elif condition.value1t == "i":
            self.assembly += "LAI " + condition.value1 + "\n"
        elif condition.value1t == "s":
            self.assembly += "LAM " + condition.value1 + "\n"

        if condition.value2 == funcParam:
            self.assembly += "LBP " + "*sp" + "\n"
        elif condition.value2t == "i":
            self.assembly += "LBI " + condition.value2 + "\n"
        elif condition.value2t == "s":
            self.assembly += "LBM " + condition.value2 + "\n"
        self.assembly += "CMP \n"
        if condition.operator == "==":
            self.assembly += "JMZ " + codeLabel + "\n"
            self.assembly += "JMP " + endLabel + "\n"
        elif condition.operator == "!=":
            self.assembly += "JMZ " + endLabel + "\n"
            self.assembly += "JMP " + codeLabel + "\n"
        elif condition.operator == ">":
            self.assembly += "JMC " + endLabel + "\n"
            self.assembly += "JMP " + codeLabel + "\n"
        elif condition.operator == "<":
            self.assembly += "JMC " + codeLabel + "\n"
            self.assembly += "JMP " + endLabel + "\n"
        elif condition.operator == "<=":
            self.assembly += "JMC " + codeLabel + "\n"
            self.assembly += "JMZ " + codeLabel + "\n"
            self.assembly += "JMP " + endLabel + "\n"
        elif condition.operator == ">=":
            self.assembly += "JMC " + endLabel + "\n"
            self.assembly += "JMZ " + codeLabel + "\n"
            self.assembly += "JMP " + codeLabel + "\n"

    def writeVar(self, cmd, param):
        if cmd.type == "o":
            self.assembly += "LAM " + cmd.value1.strip() + "\n"
            self.assembly += "OTA\n"
            return
        if cmd.type == "r":
            if checkIfParsable(cmd.value1.strip()):
                self.assembly += "LAI " + cmd.value1.strip() + "\n"
            else:
                self.assembly += "LAM " + cmd.value1.strip() + "\n"
            self.assembly += "STA return\n"
            self.assembly += "JSR " + "popa \n"
            self.assembly += "RET \n"
            return
        if cmd.type == "i":
            self.directives += "#define " + cmd.value1 + " " + str(hex(self.currentRAM)) + "\n"
            self.currentRAM += 1
        if cmd.type == "f" or cmd.type == "if":
            if cmd.type == "if":
                self.directives += "#define " + cmd.value1 + " " + str(hex(self.currentRAM)) + "\n"
                self.currentRAM += 1
            firstPar = cmd.value2.find("(")
            funcName = cmd.value2[0:firstPar]
            param = cmd.value2.replace(funcName, "").strip()
            param = getBetweenBrackets(param)
            if checkIfParsable(param):
                self.assembly += "LAI " + param + "\n"
            else:
                self.assembly += "LAM " + param + "\n"
            self.assembly += "JSR " + "pusha" + "\n"
            self.assembly += "JSR " + funcName + "\n"
            self.assembly += "LAM " + "return" + "\n"
            self.assembly += "STA " + cmd.value1 + "\n"
            return

        if any(x for x in cmd.operators if x in cmd.value2):
            vals = re.split("\W+", cmd.value2)
            ops = []
            for char in cmd.value2:
                if char == "+":
                    ops.append("+")
                elif char == "-":
                    ops.append("-")
            # print(vals, ops)
            val1 = ""
            val2 = ""
            i = 0
            for op in ops:
                if not val1:
                    val1 = vals[i]
                val2 = vals[i + 1]
                if i == 0:
                    if val1 == param:
                        self.assembly += "LAP *sp\n"  # prepare funcition to read stack to var
                    else:
                        try:
                            tr = int(val1)
                            self.assembly += "LAI " + str(tr) + "\n"
                        except:
                            self.assembly += "LAM " + str(val1) + "\n"

                if val2 == param:
                    self.assembly += "LBP *sp\n"  # prepare funcition to read stack to var
                else:
                    try:
                        tr = int(val2)
                        self.assembly += "LBI " + str(tr) + "\n"
                    except:
                        self.assembly += "LBM " + str(val2) + "\n"
                if op == "+":
                    self.assembly += "ADD\n"
                elif op == "-":
                    self.assembly += "SUB\n"
                val1 = "swap"
                i += 1
            cmd.value2 = "swap"
        if cmd.value2 != "swap":
            if cmd.value2 == param:
                self.assembly += "LAP *sp\n"  # prepare funcition to read stack to var
            else:
                try:
                    val = int(cmd.value2)
                    self.assembly += "LAI " + str(val) + "\n"
                except:
                    val = cmd.value2
                    self.assembly += "LAM " + val + "\n"
        self.assembly += "STA " + cmd.value1 + "\n"


compiler = Compiler()
