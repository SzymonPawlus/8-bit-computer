import collections
import re
from collections.abc import Iterable


class Line:
    pass


class Command(Line):
    operators = ["+", "-"]

    def __init__(self):
        self.type = ''
        self.value1 = ''
        self.value2 = ''
        self.operator = ''

    def __repr__(self):
        return "type: " + self.type + " value1: " + self.value1 + " value2: " + self.value2 + " operator: " + self.operator


class Scope(Line):
    def __init__(self):
        self.commands = []
        self.param = ""
        self.keyword = ""

    def __repr__(self):
        return "commands: " + str(self.commands) + " param: " + str(self.param) + " keyword: " + str(self.keyword)


class Lexer:
    def __init__(self, text):
        self.text = text
        self.currentChar = ''
        self.currentPosition = 0
        self.currentLine = 1
        self.commands = []
        self.currentCommand = ""
        self.currentKeyword = ""
        self.keywords = ["var"]
        self.lookWhite = False

    def lex(self):
        # check for scopes
        parsed = parse(self.text)
        parsed = join(parsed)
        parsed = divideCommands(parsed)
        # in scope divide by ";" - semicolon
        # self.text = self.text.split("\n")
        # for i in range(0, len(self.text)):
        #     self.text[i] = self.text[i].split("//")[0]
        # self.text = ''.join(self.text)
        # self.commands = self.text.split(";")
        # self.commands = [x for x in self.commands if len(x) > 0]
        # temp = []
        # for command in self.commands:
        #     com = analyzeCommand(command)
        #     temp.append(com)
        #     # print(com.toString())
        #     # print(self.commands)
        return parsed

    def error(self, text):
        raise Exception(text + " at line -> " + self.currentPosition)


def divideCommands(scoped):
    i = 0
    lines = []
    while i < len(scoped):
        cur = scoped[i]
        if isinstance(cur, str):
            cur = cur.strip()
            if cur.find("func") == 0:
                scope = Scope()
                scope.keyword = "func"
                scope.param = cur.replace("func", "").strip()
                scope.commands = divideCommands(scoped[i + 1])
                lines.append(scope)
                i += 1
            elif cur.find("if") == 0:
                scope = Scope()
                scope.keyword = "if"
                scope.param = cur.replace("if", "").strip()
                scope.commands = divideCommands(scoped[i + 1])
                lines.append(scope)
                i += 1
            elif cur.find("while") == 0:
                scope = Scope()
                scope.keyword = "while"
                scope.param = cur.replace("while", "").strip()
                scope.commands = divideCommands(scoped[i + 1])
                lines.append(scope)
                i += 1
            elif cur.find("var") == 0:
                scope = analyzeCommand(cur)
                lines.append(scope)
            elif cur.find("return") == 0:
                scope = Command()
                scope.type = "r"
                scope.value1 = cur.replace("return", "").strip()
                scope.value2 = ""
                scope.operator = "r"
                lines.append(scope)
            elif cur.find("out") == 0:
                scope = Command()
                scope.type = "o"
                scope.value1 = cur.replace("out", "").strip()
                scope.value2 = ""
                scope.operator = "o"
                lines.append(scope)
            else:
                scope = analyzeCommand(cur)
                lines.append(scope)
        else:
            pass
        i += 1
    return lines


def trimComWhite(text):
    temp = text.split("\n")
    for i in range(0, len(temp)):
        temp[i] = temp[i].split("//")[0]
    temp = ''.join(temp)
    temp = temp.split(";")
    temp = [x.strip() for x in temp]
    return [x for x in temp if len(x) > 0]


def join(l):
    string = ""
    buffer = []
    for i in range(0, len(l)):
        if isinstance(l[i], collections.Iterable) and not isinstance(l[i], str):
            string = trimComWhite(string)
            buffer += string
            string = ""
            buffer.append(join(l[i]))

        else:
            string += str(l[i])
    buffer += trimComWhite(string)
    return buffer


def parse(text):
    stack = []
    code = []
    stack.append(code)
    cur = stack[-1]
    for char in text:
        if char == '{':
            # stack push
            stack.append([])
            cur.append(stack[-1])
            cur = stack[-1]

        elif char == '}':
            stack.pop()
            cur = stack[-1]
        else:
            # stack peek
            stack[-1].append(char)
    return code


def analyzeCommand(command):
    command = command.strip()
    cmd = Command()
    if command.find("var") == 0:
        cmd.type = "i"
    else:
        cmd.type = "a"
    command = command.replace("var", "")
    command = command.strip()
    equal = command.find("=")
    if equal != -1:
        cmd.value1 = command[0:equal - 1].strip()
        cmd.value2 = command[equal + 1:].strip()
        if re.search("([.a-zA-Z]+)\(", cmd.value2):
            cmd.type += "f"
        cmd.operator = command[equal].strip()
    else:
        cmd.value1 = command
        cmd.value2 = "0"
        cmd.operator = "="
    return cmd
