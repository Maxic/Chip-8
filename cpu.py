"""
+-----------------------+
|   CHIP-8 Emulator     |
|                       |
| Barend Poot      2018 |
+-----------------------+
"""


class Cpu:
    def __init__(self):
        # memory 4kb
        self.memory = [0x00] * 4096

        # data registers (8-bit)
        self.V = [0] * 16

        # adress register (16-bit)
        self.I = 0

        # timers (8-bit)
        self.delay = 0
        self.sound = 0

        # program counter, 0x000 to 0x1FF is reserved for internal use (16-bit)
        self.pc = 0x200

        # stack pointer (8-bit) and stack (16-bit)
        self.sp = 0
        self.stack = [0] * 16

        # initialize some sprites in memory

    # fetch a single byte
    def fetch_byte(self, hexVal):
        return NotImplementedError

    print("debug")
