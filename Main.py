#!/usr/bin/env python
import minimalmodbus
import serial
import tkinter as tk            #Import Tkinter
import time

class App():
    x = 1
    instrument = minimalmodbus.Instrument('COM5', 1, minimalmodbus.MODE_RTU)  # port name, slave address (in decimal)


    def __init__(self):
        self.root = tk.Tk()                         #Bind Tkinter to the root object
        #self.root.attributes('-fullscreen', True)
        self.label = tk.Label(text="")
        self.label.pack()
        self.button1 = tk.Button(text="Go to Page One", command=self.write_slogan)
        #self.button2 = tk.Button(text="Go to Page Two", command=self.button2)
        self.button1.pack()
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

    def update_clock(self):
        now = time.time()
        # strftime("%H:%M:%S")
        if( self.x == 1 ):
            self.label.configure(text=now)
        self.root.after(100, self.update_clock)

    def write_slogan(self):
        self.instrument.write_register(0, 0)

        temperature = self.instrument.read_registers(0, 5)  # Registernumber, number of decimals

        print(temperature)



if __name__ == "__main__":
    app = App()













