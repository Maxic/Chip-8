import logging

class Cpu:
    def __init__(self):
        # memory 4kb
        self.memory = [0] * 4096

        # data registers (8-bit)
        self.V = [0] * 16

        # address register (16-bit)
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
        self.sprites = [
            0xF0, 0x90, 0x90, 0x90, 0xF0,  # Zero
            0x20, 0x60, 0x20, 0x20, 0x70,  # One
            0xF0, 0x10, 0xF0, 0x80, 0xF0,  # Two
            0xF0, 0x10, 0xF0, 0x10, 0xF0,  # Three
            0x90, 0x90, 0xF0, 0x10, 0x10,  # Four
            0xF0, 0x80, 0xF0, 0x10, 0xF0,  # Five
            0xF0, 0x80, 0xF0, 0x90, 0xF0,  # Six
            0xF0, 0x10, 0x20, 0x40, 0x40,  # Seven
            0xF0, 0x90, 0xF0, 0x90, 0xF0,  # Eight
            0xF0, 0x90, 0xF0, 0x10, 0xF0,  # Nine
            0xF0, 0x90, 0xF0, 0x90, 0x90,  # A
            0xE0, 0x90, 0xE0, 0x90, 0xE0,  # B
            0xF0, 0x80, 0x80, 0x80, 0xF0,  # C
            0xE0, 0x90, 0x90, 0x90, 0xE0,  # D
            0xF0, 0x80, 0xF0, 0x80, 0xF0,  # E
            0xF0, 0x80, 0xF0, 0x80, 0x80   # F
        ]
        # Sprites are saved in memory starting at 0x50
        for i in range(len(self.sprites)):
            self.memory[0x50+i] = self.sprites[i]

        logging.basicConfig(level=logging.INFO)

    # fetch an opcode from two bytes
    def fetch_opcode(self, hexvalue):
        byte1 = self.memory[hexvalue]
        byte2 = self.memory[hexvalue+1]
        opcode = byte1 << 8
        opcode = opcode | byte2
        self.pc += 2
        return opcode

    def execute_operation(self, opcode):
        opcode_identifier = opcode & 0xF000

        if opcode_identifier == 0x0000:
            # 00E0 - CLS - Clear the display.
            if opcode == 0x0E00:
                logging.debug(hex(opcode) + " == 00E0 - CLS - Clear the display")
                self.pc += 2

            # 00EE - RET - Return from a subroutine.
            elif opcode == 0x00EE:
                logging.debug(hex(opcode) + " == 00EE - RET - Return from a subroutine")
                self.pc += 2

        # 1nnn - JP addr - Jump to location nnn.
        elif opcode_identifier == 0x1000:
            logging.debug(hex(opcode) + " == 1nnn - JP addr - Jump to location nnn")
            self.pc += 2

        # 2nnn - CALL addr - Call subroutine at nnn.
        elif opcode_identifier == 0x2000:
            logging.debug(hex(opcode) + " == 2nnn - CALL addr - Call subroutine at nnn")
            self.pc += 2

        # 3xkk - SE Vx, byte - Skip next instruction if Vx = kk.
        elif opcode_identifier == 0x3000:
            logging.debug(hex(opcode) + " == 3xkk - SE Vx, byte - Skip next instruction if Vx = kk")
            self.pc += 2

        # 4xkk - SNE Vx, byte - Skip next instruction if Vx != kk.
        elif opcode_identifier == 0x4000:
            logging.debug(hex(opcode) + " == 4xkk - SNE Vx, byte - Skip next instruction if Vx != kk")
            self.pc += 2

        # 5xy0 - SE Vx, Vy -  Skip next instruction if Vx = Vy.
        elif opcode_identifier == 0x5000:
            logging.debug(hex(opcode) + " == 5xy0 - SE Vx, Vy -  Skip next instruction if Vx = Vy")
            self.pc += 2

        # 6xkk - LD Vx, byte - Set Vx = kk.
        elif opcode_identifier == 0x6000:
            logging.debug(hex(opcode) + " == 6xkk - LD Vx, byte - Set Vx = kk")
            self.pc += 2

        # 7xkk - ADD Vx, byte - Set Vx = Vx + kk.
        elif opcode_identifier == 0x7000:
            logging.debug(hex(opcode) + " == 7xkk - ADD Vx, byte - Set Vx = Vx + kk")
            self.pc += 2

        elif opcode_identifier == 0x8000:
            # 8xy0 - LD Vx, Vy - Set Vx = Vy.
            if opcode & 0xF == 0x0:
                logging.debug(hex(opcode) + " == 8xy0 - LD Vx, Vy - Set Vx = Vy")
                self.pc += 2

            # 8xy1 - OR Vx, Vy - Set Vx = Vx OR Vy.
            elif opcode & 0xF == 0x1:
                logging.debug(hex(opcode) + " == 8xy1 - OR Vx, Vy - Set Vx = Vx OR Vy")
                self.pc += 2

            # TODO: 8 codes
            elif opcode == 0x00EE:
                logging.debug(hex(opcode) + " == 00EE - RET - Return from a subroutine")
                self.pc += 2

        # 9xy0 - SNE Vx, Vy - Skip next instruction if Vx != Vy.
        elif opcode_identifier == 0x9000:
            logging.debug(hex(opcode) + " == 9xy0 - SNE Vx, Vy - Skip next instruction if Vx != Vy")
            self.pc += 2

        # Annn - LD I, addr - Set I = nnn.
        elif opcode_identifier == 0xA000:
            logging.debug(hex(opcode) + " == Annn - LD I, addr - Set I = nnn")
            self.pc += 2

        # Bnnn - JP V0, addr - Jump to location nnn + V0.
        elif opcode_identifier == 0xB000:
            logging.debug(hex(opcode) + " == Bnnn - JP V0, addr - Jump to location nnn + V0")
            self.pc += 2

        # Cxkk - RND Vx, byte - Set Vx = random byte AND kk.
        elif opcode_identifier == 0xC000:
            logging.debug(hex(opcode) + " == Cxkk - RND Vx, byte - Set Vx = random byte AND kk")
            self.pc += 2

        # Dxyn - DRW Vx, Vy, nibble
        # Display n-byte sprite starting at memory location I at (Vx, Vy), set VF = collision.
        elif opcode_identifier == 0xD000:
            logging.debug(hex(opcode) + " == Dxyn - DRW Vx, Vy, nibble - Display sprite and set collision")
            self.pc += 2


        else:
            logging.debug(hex(opcode) + " == " + hex(opcode))
