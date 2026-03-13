"""
Library for configuring and writing to the SparkFun SerLCD 2.5

It uses an HD44780 LCD controller behind a PIC 16F688 for the UART,
but mine doesn't respond as expected to recent HD44780 libraries.
So here is a lib that makes _my_ LCD perform as expected.
"""
import serial


class SerLCD25:
    uart: serial.Serial
    port: str

    command = 0x7C
    brightness_min = 0x80
    brightness_max = 0x9D
    extended_command = 0xFE
    extended_map = {
        "clear": 0x01,
        "display_off": 0x08,
        "display_on": 0x0C,
        "cursor_off": 0x0C,
        "cursor_box": 0x0D,
        "cursor_under": 0x0E,
        "cursor_left": 0x10,
        "cursor_right": 0x14,
        "scroll_left": 0x18,
        "scroll_right": 0x1C,
        "set_cursor": 0x80,
    }

    def __init__(self, port: str):
        self.port = port
        self.open()

    def open(self):
        self.uart = serial.Serial(
            port=self.port,
            baudrate=9600,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE
        )
        if not self.uart:
            print(f'Could not open serial port {self.port}')
            return False
        return True

    def close(self):
        self.uart.close()

    def flush(self):
        self.uart.flush()

    def write(self, command: bytes):
        self.uart.write(command)
        self.flush()

    def send(self, command: int, code: int):
        self.write(bytearray([
            command,
            code,
        ]))

    def send_command(self, code: int):
        self.send(self.command, code)

    def send_extended(self, code: int):
        self.send(self.extended_command, code)

    def send_extended_map(self, code_name: str):
        self.send_extended(self.extended_map[code_name])

    def clear(self):
        self.send_extended_map("clear")

    def display_off(self):
        self.send_extended_map("display_off")

    def display_on(self):
        self.send_extended_map("display_on")

    def cursor_off(self):
        self.send_extended_map("cursor_off")

    def cursor_box(self):
        self.send_extended_map("cursor_box")

    def cursor_under(self):
        self.send_extended_map("cursor_under")

    def cursor_left(self):
        self.send_extended_map("cursor_left")

    def cursor_right(self):
        self.send_extended_map("cursor_right")

    def scroll_left(self):
        self.send_extended_map("scroll_left")

    def scroll_right(self):
        self.send_extended_map("scroll_right")

    def set_cursor_position(self, offset: int):
        command = self.extended_map["set_cursor"] + offset
        self.send_extended(command)
