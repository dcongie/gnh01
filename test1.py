#!/usr/bin/env python
import minimalmodbus
import serial
import time

instrument = minimalmodbus.Instrument('COM5', 1, minimalmodbus.MODE_RTU) # port name, slave address (in decimal)
instrument.serial.baudrate = 9600
instrument.serial.bytesize = 8
instrument.serial.parity   = serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.serial.timeout  = 0.05   # seconds

time.sleep(2)
## Read temperature (PV = ProcessValue) ##
#temperature = instrument.read_register(1, 1) # Registernumber, number of decimals
#while(1):
instrument.write_register(0,2)
start = time.time()
temperature = instrument.read_registers(0, 5) # Registernumber, number of decimals
stop = time.time()
print (temperature)
print (stop-start)


## Change temperature setpoint (SP) ##
#NEW_TEMPERATURE = 95
#instrument.write_register(24, NEW_TEMPERATURE, 1) # Registernumber, value, number of decimals for storage