"""
working with the mcp2221 with Blinka
"""

import os

os.putenv('BLINKA_MCP2221', '1')
os.reload_environ()
import time
import serial
import board
from wiichuck.nunchuk import Nunchuk

EXPECTED_BOARD = 'MICROCHIP_MCP2221'
PORT = "/dev/ttyACM0"
LOG = True

found_board = board.board_id

def log(msg):
    if LOG:
        print(msg)

print("Starting...")

log(found_board)
if found_board != EXPECTED_BOARD:
    print(f'{EXPECTED_BOARD} NOT Found, exiting')
    quit()

ser = serial.Serial(
    port=(f"{PORT}"),
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE
)

if not ser:
    print(f'No UART connected at {PORT}, exiting')
    quit()


def cc(code):
    ser.write(b'\x7C' + code)
    ser.flush()


def ec(code):
    ser.write(b'\xFE' + code)
    ser.flush()


def clear():
    ec(b'\x01')


def w(msg):
    if type(msg) != (bytes or bytearray):
        msg = msg.encode()
    ser.write(msg)
    ser.flush()


def cw(msg):
    clear()
    w(msg)


def p(msg):
    log(msg)
    w(msg)


def cp(msg):
    log(msg)
    cw(msg)

nc = None
found = False
while not found:
    try:
        cp("Connecting...")
        bus = board.I2C()
        # more reliably detect the nunchuk by resetting the i2c bus
        bus.deinit()
        bus = board.I2C()

        devs = []
        for i in range(1, 4):
            cp(f'Scanning ({i})...')
            devs = [hex(dev) for dev in bus.scan()]
            print(devs)
            if devs:
                break
            print('Scanning again')

        nc_addr = '0x52'
        if nc_addr in devs:
            cp(f'Nunchuk at {nc_addr}')
            found = True
        else:
            cp('No Nunchuk found')
            quit()

        nc = Nunchuk(board.I2C())
    except (OSError, RuntimeError) as e:
        log(e)

def display():
    x, y = nc.joystick
    ax, ay, az = nc.acceleration

    log("joystick = {},{}".format(x, y))
    log("acceleration ax={}, ay={}, az={}".format(ax, ay, az))

    buttons = ""
    if nc.buttons.Z:
        log("button Z")
        buttons += "Z"
    if nc.buttons.C:
        log("button C")
        buttons += "C"

    line_one = f'J:{str(x).zfill(3)},{str(y).zfill(3)} B:{buttons}'
    l = 16 - len(line_one)
    line_one += ' ' * l
    line_two = f'A:[{ax},{ay},{az}]'
    cw(line_one + line_two)

log("Running...")

try:
    display()
    LOG = False
    while True:
        display()

        time.sleep(0.001)
except KeyboardInterrupt:
    pass

LOG = True
log("Done")
