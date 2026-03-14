"""
Working with the MCP2221, SerLCD 2.5, and Wii Nunchuks, with Blinka
"""


EXPECTED_BOARD = 'MICROCHIP_MCP2221'
PORT = '/dev/ttyACM0'
I2C_ATTEMPTS = 4
NUNCHUK_ADDRESS = '0x52'
LCD_UPDATE_DELAY = 0.01

import os
os.putenv('BLINKA_MCP2221', '1')
os.reload_environ()
import time

import board
from wiichuck.nunchuk import Nunchuk

import SerLCD25

serial: SerLCD25.SerLCD25


def show(msg):
    global ser
    print(msg)
    ser.clear()
    ser.write(msg.encode())


print('Connecting to board')
found_board = board.board_id
print(f'Found board: {found_board}')
if found_board != EXPECTED_BOARD:
    print(f'{EXPECTED_BOARD} NOT Found, exiting')
    quit()

print('Connecting to UART')
ser = SerLCD25.SerLCD25(port=PORT)
if not ser:
    print(f'No UART connected at {PORT}, exiting')
    quit()

print('Connecting to I2C')
nc = None
found = False
attempts = 0
while not found:
    time.sleep(1)
    if attempts >= I2C_ATTEMPTS:
        print('Attempts exceeded, exiting')
        break
    attempts += 1

    try:
        show(f'{attempts}: Connecting')
        bus = board.I2C()

        show(f'{attempts}: Scanning')
        devs = [hex(dev) for dev in bus.scan()]
        if not devs:
            show(f'{attempts}: No devices found')
            continue
        print(f'Devices found: {devs}')

        if NUNCHUK_ADDRESS not in devs:
            show(f'{attempts}: No Nunchuks found')
            continue

        nc = Nunchuk(board.I2C())
        show(f'Nunchuk at {NUNCHUK_ADDRESS}')
        found = True
    except (OSError, RuntimeError) as e:
        show('Error: {e}')

time.sleep(1)

if not found:
    show(f'{attempts}: No Nunchuks')
    print(f'No Nunchuks found after {attempts} attempts, exiting')
    quit()

print('Running...')
try:
    while True:
        x, y = nc.joystick
        ax, ay, az = nc.acceleration

        z, c = nc.buttons
        buttons = f'[{"Z" if z else " "}{"C" if c else " "}]'

        line_one = f'J:{str(x).zfill(3)},{str(y).zfill(3)} B:{buttons}'
        l = 16 - len(line_one)
        line_one += ' ' * l
        line_two = f'A:[{ax},{ay},{az}]'
        ser.clear()
        ser.write((line_one + line_two).encode())

        if True:
            print(line_one)
            print(line_two)

        time.sleep(LCD_UPDATE_DELAY)
except KeyboardInterrupt:
    pass

print('Done')
