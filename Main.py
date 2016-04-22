#!/usr/bin/env python
import minimalmodbus
import serial
import tkinter as tk            #Import Tkinter
import time

class App():
    #const
    MODBUS_MODE = 0x00
    MODBUS_ALARM = 0x23
    CONST_CMV_MODE = 0
    CONST_AC_MODE = 1
    CONST_SIMV_MODE = 2
    CONST_ALARM_HIGH_PRESSURE = 0x01
    CONST_ALARM_LOW_PRESSURE = 0x02
    CONST_ALARM_LOW_BATTERY = 0x04
    CONST_ALARM_LOW_OXYGEN = 0x08
    CONST_ALARM_HIGH_FREQ = 0x10

    timer1 = 0

    #always updated
    Mode = 0
    pressure = 0
    ftol = 0
    alarm = 0
    battery = 0

    #CMV
    cmv_tidal_volume = 0
    cmv_resp_rate = 0
    cmv_fio2 = 0
    cmv_high_pressure_limit = 0
    cmv_high_frequency_limit = 0
    cmv_low_pressure_limit = 0

    #AC
    ac_tidal_volume = 0
    ac_trigger_pressure = 0
    ac_pmax = 0
    ac_resp_rate = 0
    ac_fio2 = 0
    ac_high_pressure_limit = 0
    ac_high_frequency_limit = 0
    ac_low_pressure_limit = 0

    #SIMV
    simv_tidal_volume = 0
    simv_trigger_pressure = 0
    simv_pmax = 0
    simv_resp_rate = 0
    simv_fio2 = 0
    simv_high_pressure_limit = 0
    simv_high_frequency_limit = 0
    simv_low_pressure_limit = 0

    x = 1
    instrument = minimalmodbus.Instrument('COM5', 1, minimalmodbus.MODE_RTU)  # port name, slave address (in decimal)


    def __init__(self):
        self.root = tk.Tk()                         #Bind Tkinter to the root object
        #self.root.attributes('-fullscreen', True)
        self.l_mode = tk.Label(text="")
        self.l_mode.pack()
        self.l_alarm = tk.Label(text="")
        self.l_alarm.pack()
        self.l_pressure = tk.Label(text="")
        self.l_pressure.pack()
        self.l_ftol = tk.Label(text="")
        self.l_ftol.pack()

        self.label = tk.Label(text="")
        self.label.pack()

        self.button_cmv = tk.Button(text="CMV", command=self.enter_cmv_mode)
        self.button_cmv.pack()
        self.button_ac = tk.Button(text="AC", command=self.enter_ac_mode)
        self.button_ac.pack()
        self.button_simv = tk.Button(text="SIMV", command=self.enter_simv_mode)
        self.button_simv.pack()
        self.button_clear = tk.Button(text="Clear Alarm", command=self.clear_alarm)
        self.button_clear.pack()

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

    def read_cmv(self):
        read_cmv = self.instrument.read_registers(0x01, 7)
        print("[01h] %s" % read_cmv)


#    def read_ac(self):

#    def read_simv(self):

    def read_parameters(self):
        #read mode
        read_mode = self.instrument.read_registers(self.MODBUS_MODE, 1)
        print("[00h] %s" % read_mode)
        self.Mode = read_mode[0]
        if (self.Mode == self.CONST_CMV_MODE):
            self.l_mode.config(text="CMV Mode")
            self.read_cmv()
        elif (self.Mode == self.CONST_AC_MODE):
            self.l_mode.config(text="AC Mode")
         #   read_ac()
        elif (self.Mode == self.CONST_SIMV_MODE):
            self.l_mode.config(text="SIMV Mode")
        #    read_simv()

    def read_regular(self):
        # read_always
        read_always = self.instrument.read_registers(0x20, 4)
        print("[20h] %s" % read_always)
        self.pressure = read_always[0] - 20
        self.ftol = read_always[1]
        self.alarm = read_always[3]

    def update_alarm(self):
        res = ""
        if( (self.alarm & self.CONST_ALARM_HIGH_PRESSURE) == self.CONST_ALARM_HIGH_PRESSURE):
            res += "High Airway Pressure Limit! "
        if( (self.alarm & self.CONST_ALARM_LOW_PRESSURE) == self.CONST_ALARM_LOW_PRESSURE):
            res += "Low Airway Pressure Limit! "
        if( (self.alarm & self.CONST_ALARM_LOW_BATTERY) == self.CONST_ALARM_LOW_BATTERY):
            res += "Low Battery! "
        if( (self.alarm & self.CONST_ALARM_LOW_OXYGEN) == self.CONST_ALARM_LOW_OXYGEN):
            res += "Low Oxygen! "
        if( (self.alarm & self.CONST_ALARM_HIGH_FREQ) == self.CONST_ALARM_HIGH_FREQ):
            res += "High Frequency! "
        self.l_alarm.config(text=res)



    def update_clock(self):
        self.timer1 = self.timer1 + 1
        if( self.timer1 >= 10):
            self.timer1 = 0
            self.read_parameters()

        self.read_regular()
        self.update_alarm()




        now = time.time()
        # strftime("%H:%M:%S")
        if( self.x == 1 ):
            self.label.configure(text=now)
        self.root.after(100, self.update_clock)

    def enter_cmv_mode(self):
        self.instrument.write_register(self.MODBUS_MODE, self.CONST_CMV_MODE)

    def enter_ac_mode(self):
        self.instrument.write_register(self.MODBUS_MODE, self.CONST_AC_MODE)

    def enter_simv_mode(self):
        self.instrument.write_register(self.MODBUS_MODE, self.CONST_SIMV_MODE)

    def clear_alarm(self):
        self.instrument.write_register(self.MODBUS_ALARM, 0)

if __name__ == "__main__":
    app = App()













