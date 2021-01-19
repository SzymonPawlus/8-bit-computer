import sys
import numpy as np

from computer import Computer
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QCheckBox, QSlider
from PyQt5.QtCore import Qt
import threading

sys.tracebacklimit = 0

if len(sys.argv) < 2:
    raise ValueError("Not enough arguments")


# Subclass QMainWindow to customise your application's main window
class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setFixedSize(1000, 600)
        self.setWindowTitle("Platfus Computer Emulator")

        self.ROMlabel = self.createLabel("ROM", (10, 10))

        self.box = QCheckBox("Start", self)
        self.box.move(30 + 40 * 18, 10)
        self.box.show()

        self.button2 = QPushButton("Tick", self)
        self.button2.move(30 + 40 * 18, 50)
        self.button2.clicked.connect(self.tick)
        self.button2.show()

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMinimum(10)
        self.slider.setMaximum(500)
        self.slider.move(30 + 40 * 18, 90)
        self.slider.show()

        self.computer = Computer()

        self.outLabel = self.createLabel("Output", (30 + 40 * 18, 130))
        self.outValue = self.createLabel("0", (30 + 40 * 18, 150))

        self.ALabel = self.createLabel("A", (30 + 40 * 18, 190))
        self.AValue = self.createLabel("0", (30 + 40 * 18, 210))

        self.BLabel = self.createLabel("B", (30 + 40 * 20, 190))
        self.BValue = self.createLabel("0", (30 + 40 * 20, 210))

        self.cmdLabel = self.createLabel("Command", (30 + 40 * 18, 250))
        self.cmdValue = self.createLabel("", (30 + 40 * 18, 270))

        self.ZLabel = self.createLabel("Zero", (30 + 40 * 18, 310))
        self.ZValue = self.createLabel("0", (30 + 40 * 18, 330))

        self.CLabel = self.createLabel("Carry", (30 + 40 * 20, 310))
        self.CValue = self.createLabel("0", (30 + 40 * 20, 330))

        self.SPLabel = self.createLabel("Stack Pointer", (30 + 40 * 18, 370))
        self.SPValue = self.createLabel("0", (30 + 40 * 18, 390))

        self.PCLabel = self.createLabel("P. Counter", (30 + 40 * 18, 430))
        self.PCValue = self.createLabel("0", (30 + 40 * 18, 450))

        self.exit = False

        Bytes = np.fromfile(sys.argv[1], "uint8")
        x = 0
        for byte in Bytes:
            self.computer.MEM[x] = byte
            x += 1

        x = 50
        y = 10
        i = 0
        j = 0
        self.labels = []

        for label in range(0, 16):
            label = QLabel(str(hex(j)), self)
            label.move(x, y)
            label.setFixedSize(40, 30)
            if i == 15:
                i = -1
                x = 10
                y += 30
            label.show()
            x += 40
            i += 1
            j += 1

        u = 0
        for label in range(0, 192):
            if i == 0:
                address = QLabel(str(hex(u)), self)
                address.move(10, y)
                address.show()
                u += 1
            label = QLabel("0x00", self)
            label.move(x, y)
            label.setFixedSize(40, 30)
            if i == 15:
                i = -1
                x = 10
                y += 30
            label.show()
            x += 40
            i += 1
            self.labels.append(label)

        self.RAMlabel = self.createLabel("RAM", (10, y))
        y += 30

        for label in range(0, 64):
            if i == 0:
                address = QLabel(str(hex(u)), self)
                address.move(10, y)
                address.show()
                u += 1
            label = QLabel("0x00", self)
            label.setFixedSize(40, 30)
            label.move(x, y)
            if i == 15:
                i = -1
                x = 10
                y += 30
            label.show()
            x += 40
            i += 1
            self.labels.append(label)

        self.clock()

    def clock(self):
        if not self.exit:
            threading.Timer(1 / self.slider.value(), self.clock).start()
            if self.box.isChecked():
                self.tick()

    def tick(self):
        #if self.slider.value() < 60:
          #  self.labels[self.computer.Counter].setStyleSheet("background-color: rgba(0, 0, 0, 0);")
          #  self.labels[self.computer.stackPointer].setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.computer.clock()
        self.outValue.setText(str(self.computer.output))
        self.AValue.setText(str(self.computer.A))
        self.BValue.setText(str(self.computer.B))
        self.ZValue.setText(str(self.computer.ZF))
        self.CValue.setText(str(self.computer.CF))
        self.SPValue.setText(str(self.computer.stackPointer))
        self.PCValue.setText(str(self.computer.Counter))
        self.cmdValue.setText(str(self.computer.commandsLabels[self.computer.MEM[self.computer.Counter]]) + " " + str(
            self.computer.MEM[self.computer.Counter + 1]))
        x = 0
        for byte in self.computer.MEM:
            self.labels[x].setText(str(byte))
            #if x == self.computer.Counter and self.slider.value() < 60:
             #   self.labels[x].setStyleSheet("background-color: red;")
           # if x == self.computer.stackPointer and self.slider.value() < 60:
            #    self.labels[x].setStyleSheet("background-color: blue;")

            x += 1

    def createLabel(self, text, position):
        label = QLabel(text, self)
        label.move(position[0], position[1])
        label.show()
        return label

    def closing(self):
        self.exit = True


app = QApplication(sys.argv)

window = MainWindow()
window.show()
app.setQuitOnLastWindowClosed(True)
app.lastWindowClosed.connect(window.closing)
sys.exit(app.exec_())
