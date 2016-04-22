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

    timer1 = 9

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

        self.label1 = tk.Label(text="")
        self.label1.pack()
        self.label2 = tk.Label(text="")
        self.label2.pack()
        self.label3 = tk.Label(text="")
        self.label3.pack()
        self.label4 = tk.Label(text="")
        self.label4.pack()
        self.label5 = tk.Label(text="")
        self.label5.pack()
        self.label6 = tk.Label(text="")
        self.label6.pack()
        self.label7 = tk.Label(text="")
        self.label7.pack()
        self.label8 = tk.Label(text="")
        self.label8.pack()

        self.button_cmv = tk.Button(text="CMV", command=self.enter_cmv_mode)
        self.button_cmv.pack()
        self.button_ac = tk.Button(text="AC", command=self.enter_ac_mode)
        self.button_ac.pack()
        self.button_simv = tk.Button(text="SIMV", command=self.enter_simv_mode)
        self.button_simv.pack()
        self.button_clear = tk.Button(text="Clear Alarm", command=self.clear_alarm)
        self.button_clear.pack()

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

    def to_hpa(self, pressure):
        return (pressure -200) / 10.0

    def read_cmv(self):
        read_cmv = self.instrument.read_registers(0x01, 7)
        print("[01h] %s" % read_cmv)
        self.cmv_tidal_volume = read_cmv[0] * 10
        self.cmv_resp_rate = read_cmv[1]
        self.cmv_fio2 = read_cmv[2] * 10
        self.cmv_high_pressure_limit = self.to_hpa(read_cmv[4])
        self.cmv_low_pressure_limit = self.to_hpa(read_cmv[5])
        self.cmv_high_frequency_limit = read_cmv[6]
        self.label1.config(text="Tidal Volume: " + str(self.cmv_tidal_volume) + "ml")
        self.label2.config(text="Respiratory Rate: " + str(self.cmv_resp_rate) + " per minute")
        self.label3.config(text="FIO2: " + str(self.cmv_fio2) + "%")
        self.label4.config(text="High Pressure Limit: " + str(self.cmv_high_pressure_limit) + "hPa")
        self.label5.config(text="Low Pressure Limit: " + str(self.cmv_low_pressure_limit) + "hPa")
        self.label6.config(text="High Frequency Limit: " + str(self.cmv_high_frequency_limit) + "bpm")
        self.label7.config(text="")
        self.label8.config(text="")

    def read_ac(self):
        read_ac = self.instrument.read_registers(0x08, 8)
        print("[08h] %s" % read_ac)
        self.ac_tidal_volume = read_ac[0] * 10
        self.ac_trigger_pressure = self.to_hpa(read_ac[1])
        self.ac_pmax = self.to_hpa((read_ac[2]))
        self.ac_resp_rate = read_ac[3]
        self.ac_fio2 = read_ac[4] * 10
        self.ac_high_pressure_limit = self.to_hpa(read_ac[5])
        self.ac_low_pressure_limit = self.to_hpa(read_ac[6])
        self.ac_high_frequency_limit = read_ac[7]
        self.label1.config(text="Tidal Volume: " + str(self.ac_tidal_volume) + "ml")
        self.label2.config(text="Trigger: " + str(self.ac_trigger_pressure) + "hPa")
        self.label3.config(text="Max Pressure: " + str(self.ac_pmax) + "hPa")
        self.label4.config(text="Respiratory Rate: " + str(self.ac_resp_rate) + " per minute")
        self.label5.config(text="FIO2: " + str(self.ac_fio2) + "%")
        self.label6.config(text="High Pressure Limit: " + str(self.ac_high_pressure_limit) + "hPa")
        self.label7.config(text="Low Pressure Limit: " + str(self.ac_low_pressure_limit) + "hPa")
        self.label8.config(text="High Frequency Limit: " + str(self.ac_high_frequency_limit) + "bpm")

    def read_simv(self):
        read_simv = self.instrument.read_registers(0x10, 8)
        print("[08h] %s" % read_simv)
        self.simv_tidal_volume = read_simv[0] * 10
        self.simv_trigger_pressure = self.to_hpa(read_simv[1])
        self.simv_pmax = self.to_hpa((read_simv[2]))
        self.simv_resp_rate = read_simv[3]
        self.simv_fio2 = read_simv[4] * 10
        self.simv_high_pressure_limit = self.to_hpa(read_simv[5])
        self.simv_low_pressure_limit = self.to_hpa(read_simv[6])
        self.simv_high_frequency_limit = read_simv[7]
        self.label1.config(text="Tidal Volume: " + str(self.simv_tidal_volume) + "ml")
        self.label2.config(text="Trigger: " + str(self.simv_trigger_pressure) + "hPa")
        self.label3.config(text="Max Pressure: " + str(self.simv_pmax) + "hPa")
        self.label4.config(text="Respiratory Rate: " + str(self.simv_resp_rate) + " per minute")
        self.label5.config(text="FIO2: " + str(self.simv_fio2) + "%")
        self.label6.config(text="High Pressure Limit: " + str(self.simv_high_pressure_limit) + "hPa")
        self.label7.config(text="Low Pressure Limit: " + str(self.simv_low_pressure_limit) + "hPa")
        self.label8.config(text="High Frequency Limit: " + str(self.simv_high_frequency_limit) + "bpm")

    def read_parameters(self):
        #read mode
        read_mode = self.instrument.read_registers(self.MODBUS_MODE, 1)
        print("[00h]", read_mode)
        self.Mode = read_mode[0]
        if (self.Mode == self.CONST_CMV_MODE):
            self.l_mode.config(text="CMV Mode")
            self.read_cmv()
        elif (self.Mode == self.CONST_AC_MODE):
            self.l_mode.config(text="AC Mode")
            self.read_ac()
        elif (self.Mode == self.CONST_SIMV_MODE):
            self.l_mode.config(text="SIMV Mode")
            self.read_simv()

    def read_regular(self):
        # read_always
        read_always = self.instrument.read_registers(0x20, 4)
        print("[20h]", read_always)
        self.pressure = self.to_hpa(read_always[0])
        self.ftol = read_always[1]
        self.alarm = read_always[3]
        self.l_pressure.config(text="PAW: " + str(self.pressure) + "hPa")
        self.l_ftol.config(text="FTOL: " + str(self.ftol) + "bpm")

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













