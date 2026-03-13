#!/usr/env/bin python
"""
testing old SparkFun SerLCD 2.5 16x2 display over UART
"""

import EasyMCP2221
import serial

# mcp = EasyMCP2221.Device()
# mcp.reset(1.0)

ser = serial.Serial(
    port="/dev/ttyACM0",
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE
)

def CC(code):
    ser.write(b'\x7C' + code)
    ser.flush()

def EC(code):
    ser.write(b'\xFE' + code)
    ser.flush()

def W(msg):
    ser.write(msg)
    ser.flush()

# set 16x2
# CC(4)
# CC(6)

EC(b'\x01')

CC(b'\127')

W('Hello World!'.encode('utf-8'))
