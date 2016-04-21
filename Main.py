#!/usr/bin/env python
import minimalmodbus
import serial
import tkinter as tk            #Import Tkinter
import time

class App():
    CONST_CMV_MODE = 0
    CONST_AC_MODE = 1
    CONST_SIMV_MODE = 2
    timer1 = 0
    Mode = 0

    x = 1
    instrument = minimalmodbus.Instrument('COM5', 1, minimalmodbus.MODE_RTU)  # port name, slave address (in decimal)


    def __init__(self):
        self.root = tk.Tk()                         #Bind Tkinter to the root object
        #self.root.attributes('-fullscreen', True)
        self.l_mode = tk.Label(text="1")
        self.l_mode.pack()
        self.label = tk.Label(text="")
        self.label.pack()
        self.button_cmv = tk.Button(text="CMV", command=self.enter_cmv_mode)
        self.button_cmv.pack()
        self.button_ac = tk.Button(text="AC", command=self.enter_ac_mode)
        self.button_ac.pack()
        self.button_simv = tk.Button(text="SIMV", command=self.enter_simv_mode)
        self.button_simv.pack()

        #self.button2 = tk.Button(text="Go to Page Two", command=self.button2)

        #self.button2.pack()
        self.init_modbus()
        self.update_clock()
        self.root.mainloop()

    def init_modbus(self):
        self.instrument.serial.baudrate = 9600
        self.instrument.serial.bytesize = 8
        self.instrument.serial.parity = serial.PARITY_NONE
        self.instrument.serial.stopbits = 1
        self.instrument.serial.timeout = 0.05  # seconds
        time.sleep(2)

    def read_parameters(self):
        #read mode
        read_mode = self.instrument.read_registers(0, 1)
        print("[0] %s" % read_mode)
        self.Mode = read_mode[0]

    def update_clock(self):
        self.timer1 = self.timer1 + 1
        if( self.timer1 >= 10):
            self.timer1 = 0
            self.read_parameters()



        if (self.Mode == self.CONST_CMV_MODE):
            self.l_mode.config(text="CMV Mode")
        elif (self.Mode == self.CONST_AC_MODE):
            self.l_mode.config(text="AC Mode")
        elif (self.Mode == self.CONST_SIMV_MODE):
            self.l_mode.config(text="SIMV Mode")

        now = time.time()
        # strftime("%H:%M:%S")
        if( self.x == 1 ):
            self.label.configure(text=now)
        self.root.after(100, self.update_clock)

    def enter_cmv_mode(self):
        self.instrument.write_register(0, self.CONST_CMV_MODE)

    def enter_ac_mode(self):
        self.instrument.write_register(0, self.CONST_AC_MODE)

    def enter_simv_mode(self):
        self.instrument.write_register(0, self.CONST_SIMV_MODE)

    def write_slogan(self):
        #self.instrument.write_register(0, 0)
        temperature = self.instrument.read_registers(0, 5)  # Registernumber, number of decimals
        print(temperature)



if __name__ == "__main__":
    app = App()













