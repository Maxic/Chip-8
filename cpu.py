import logging
import random
import numpy as N


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
        self.stack_pointer = 0
        self.stack = [0] * 16

        # Initialize graphics array
        self.graphics = N.zeros((31, 63))

        # initialize some sprites in memory
        self.sprite_pointer = 0x50
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
            self.memory[self.sprite_pointer+i] = self.sprites[i]

        logging.basicConfig(level=logging.DEBUG)

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
        nnn = opcode & 0xFFF
        kk = opcode & 0x00FF
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4

        # 0XXX -  Multiple opcodes
        if opcode_identifier == 0x0000:
            # 00E0 - CLS - Clear the display.
            if opcode == 0x0E00:
                logging.debug(hex(opcode) + " == 00E0 - CLS - Clear the display")
                self.graphics = N.zeros((31, 63))
                self.pc += 2

            # 00EE - RET - Return from a subroutine.
            elif opcode == 0x00EE:
                logging.debug(hex(opcode) + " == 00EE - RET - Return from a subroutine")
                self.pc = self.stack[self.stack_pointer]
                self.stack_pointer -= 1

        # 1nnn - JP addr - Jump to location nnn.
        elif opcode_identifier == 0x1000:
            logging.debug(hex(opcode) + " == 1nnn - JP addr - Jump to location nnn")
            self.pc = nnn

        # 2nnn - CALL addr - Call subroutine at nnn.
        elif opcode_identifier == 0x2000:
            logging.debug(hex(opcode) + " == 2nnn - CALL addr - Call subroutine at nnn")
            self.stack_pointer += 1
            self.stack[self.stack_pointer] = self.pc
            self.pc = nnn

        # 3xkk - SE Vx, byte - Skip next instruction if Vx = kk.
        elif opcode_identifier == 0x3000:
            logging.debug(hex(opcode) + " == 3xkk - SE Vx, byte - Skip next instruction if Vx = kk")
            if self.V[x] == kk:
                self.pc += 4
            else:
                self.pc += 2

        # 4xkk - SNE Vx, byte - Skip next instruction if Vx != kk.
        elif opcode_identifier == 0x4000:
            logging.debug(hex(opcode) + " == 4xkk - SNE Vx, byte - Skip next instruction if Vx != kk")
            if self.V[x] != kk:
                self.pc += 4
            else:
                self.pc += 2

        # 5xy0 - SE Vx, Vy -  Skip next instruction if Vx = Vy.
        elif (opcode_identifier == 0x5000) and (opcode & 0xF == 0x0):
            logging.debug(hex(opcode) + " == 5xy0 - SE Vx, Vy -  Skip next instruction if Vx = Vy")
            if self.V[x] == self.V[y]:
                self.pc += 4
            else:
                self.pc += 2
            self.pc += 2

        # 6xkk - LD Vx, byte - Set Vx = kk.
        elif opcode_identifier == 0x6000:
            logging.debug(hex(opcode) + " == 6xkk - LD Vx, byte - Set Vx = kk")
            self.V[x] = kk
            self.pc += 2

        # 7xkk - ADD Vx, byte - Set Vx = Vx + kk.
        elif opcode_identifier == 0x7000:
            logging.debug(hex(opcode) + " == 7xkk - ADD Vx, byte - Set Vx = Vx + kk")
            self.V[x] = self.V[x] + kk
            self.pc += 2

        # 8XXX - Multiple opcodes
        elif opcode_identifier == 0x8000:
            # 8xy0 - LD Vx, Vy - Set Vx = Vy.
            if opcode & 0xF == 0x0:
                logging.debug(hex(opcode) + " == 8xy0 - LD Vx, Vy - Set Vx = Vy")
                self.V[x] = self.V[y]
                self.pc += 2

            # 8xy1 - OR Vx, Vy - Set Vx = Vx OR Vy.
            elif opcode & 0xF == 0x1:
                logging.debug(hex(opcode) + " == 8xy1 - OR Vx, Vy - Set Vx = Vx OR Vy")
                self.V[x] = self.V[x] | self.V[y]
                self.pc += 2

            # 8xy2 - AND Vx, Vy - Set Vx = Vx AND Vy.
            elif opcode & 0xF == 0x2:
                logging.debug(hex(opcode) + " == 8xy2 - AND Vx, Vy - Set Vx = Vx AND Vy")
                self.V[x] = self.V[x] & self.V[y]
                self.pc += 2

            # 8xy3 - XOR Vx, Vy - Set Vx = Vx XOR Vy.
            elif opcode & 0xF == 0x3:
                logging.debug(hex(opcode) + " == 8xy3 - XOR Vx, Vy - Set Vx = Vx XOR Vy")
                self.V[x] = self.V[x] ^ self.V[y]
                self.pc += 2

            # 8xy4 - ADD Vx, Vy - Set Vx = Vx + Vy, set VF = carry.
            elif opcode & 0xF == 0x4:
                logging.debug(hex(opcode) + " == xy4 - ADD Vx, Vy - Set Vx = Vx + Vy, set VF = carry")
                if self.V[x] + self.V[y] > 0xFF:
                    self.V[0xF] = 1
                    self.V[x] = (self.V[x] + self.V[y]) - 256
                else:
                    self.V[0xF] = 0
                    self.V[x] = self.V[x] + self.V[y]
                self.pc += 2

            # 8xy5 - SUB Vx, Vy - Set Vx = Vx - Vy, set VF = NOT borrow.
            elif opcode & 0xF == 0x5:
                logging.debug(hex(opcode) + " == 8xy5 - SUB Vx, Vy - Set Vx = Vx - Vy, set VF = NOT borrow")
                if self.V[x] > self.V[y]:
                    self.V[0xF] = 1
                else:
                    self.V[0xF] = 0
                self.V[x] = self.V[x] - self.V[y]
                self.pc += 2

            # 8xy6 - SHR Vx {, Vy} - Set Vx = Vx SHR 1.
            elif opcode & 0xF == 0x6:
                logging.debug(hex(opcode) + " == 8xy6 - SHR Vx {, Vy} - Set Vx = Vx SHR 1")
                if self.V[x] & 0x1 == 1:
                    self.V[0xF] = 1
                else:
                    self.V[0xF] = 0
                self.V[x] = self.V[x] / 2
                self.pc += 2

            # 8xy7 - SUBN Vx, Vy - Set Vx = Vy - Vx, set VF = NOT borrow.
            elif opcode & 0xF == 0x7:
                logging.debug(hex(opcode) + " == 8xy7 - SUBN Vx, Vy - Set Vx = Vy - Vx, set VF = NOT borrow")
                if self.V[y] > self.V[x]:
                    self.V[0xF] = 1
                else:
                    self.V[0xF] = 0
                self.V[x] = self.V[y] - self.V[x]
                self.pc += 2

            # 8xyE - SHL Vx {, Vy} - Set Vx = Vx SHL 1.
            elif opcode & 0xF == 0xE:
                logging.debug(hex(opcode) + " == 8xyE - SHL Vx {, Vy} - Set Vx = Vx SHL 1")
                if self.V[x] & 0x80 >> 7 == 1:
                    self.V[0xF] = 1
                else:
                    self.V[0xF] = 0
                self.V[x] = self.V[x] * 2
                self.pc += 2

        # 9xy0 - SNE Vx, Vy - Skip next instruction if Vx != Vy.
        elif (opcode_identifier == 0x9000) and (opcode & 0xF == 0x0):
            logging.debug(hex(opcode) + " == 9xy0 - SNE Vx, Vy - Skip next instruction if Vx != Vy")
            if self.V[x] != self.V[y]:
                self.pc += 4
            else:
                self.pc += 2

        # Annn - LD I, addr - Set I = nnn.
        elif opcode_identifier == 0xA000:
            logging.debug(hex(opcode) + " == Annn - LD I, addr - Set I = nnn")
            self.I = nnn
            self.pc += 2

        # Bnnn - JP V0, addr - Jump to location nnn + V0.
        elif opcode_identifier == 0xB000:
            logging.debug(hex(opcode) + " == Bnnn - JP V0, addr - Jump to location nnn + V0")
            self.pc = nnn + self.V[0]
            self.pc += 2

        # Cxkk - RND Vx, byte - Set Vx = random byte AND kk.
        elif opcode_identifier == 0xC000:
            logging.debug(hex(opcode) + " == Cxkk - RND Vx, byte - Set Vx = random byte AND kk")
            random_byte = random.randint(0, 255)
            self.V[x] = random_byte & kk
            self.pc += 2

        # Dxyn - DRW Vx, Vy, nibble # TODO
        # Display n-byte sprite starting at memory location I at (Vx, Vy), set VF = collision.
        elif opcode_identifier == 0xD000:
            logging.debug(hex(opcode) + " == Dxyn - DRW Vx, Vy, nibble - Display sprite and set collision")
            self.pc += 2

        #EXXX - Multiple opcodes
        elif opcode_identifier == 0xE000:
            # Ex9E - SKP Vx - Skip next instruction if key with the value of Vx is pressed. # TODO
            if (opcode & 0xF0FF) == 0xE091:
                logging.debug(hex(opcode) + " == Ex9E - SKP Vx - Skip next instruction if key with the value of Vx is pressed")
                self.pc += 2

            # ExA1 - SKNP Vx - Skip next instruction if key with the value of Vx is not pressed. # TODO
            elif opcode & 0xF0FF == 0xE0A1:
                logging.debug(hex(opcode) + " == ExA1 - SKNP Vx - Skip next instruction if key with the value of Vx is not pressed")
                self.pc += 2

        # FXXX - Multiple opcodes
        elif opcode_identifier == 0xF000:

            # Fx07 - LD Vx, DT - Set Vx = delay timer value.
            if opcode & 0xF0FF == 0xF007:
                logging.debug(hex(opcode) + " == Fx07 - LD Vx, DT - Set Vx = delay timer value")
                self.V[x] = self.delay
                self.pc += 2

            # Fx0A - LD Vx, K - Wait for a key press, store the value of the key in Vx. # TODO
            elif opcode & 0xF0FF == 0xF00A:
                logging.debug(hex(opcode) + " == Fx0A - LD Vx, K - Wait for a key press, store the value of the key in Vx")
                self.pc += 2

            # Fx15 - LD DT, Vx - Set delay timer = Vx.
            elif opcode & 0xF0FF == 0xF015:
                logging.debug(hex(opcode) + " == Fx15 - LD DT, Vx - Set delay timer = Vx")
                self.delay = self.V[x]
                self.pc += 2

            # Fx18 - LD ST, Vx - Set sound timer = Vx.
            elif opcode & 0xF0FF == 0xF018:
                logging.debug(hex(opcode) + " == Fx18 - LD ST, Vx - Set sound timer = Vx")
                self.sound = self.V[x]
                self.pc += 2

            # Fx1E - ADD I, Vx - Set I = I + Vx. #
            elif opcode & 0xF0FF == 0xF01E:
                logging.debug(hex(opcode) + " == Fx1E - ADD I, Vx - Set I = I + Vx")
                self.I = self.I + self.V[x]
                self.pc += 2

            # Fx29 - LD F, Vx - Set I = location of sprite for digit Vx.
            elif opcode & 0xF0FF == 0xF029:
                logging.debug(hex(opcode) + " == Fx29 - LD F, Vx - Set I = location of sprite for digit Vx")
                self.I = (self.V[x] * 5) + self.sprite_pointer
                self.pc += 2

            # Fx33 - LD B, Vx - Store BCD representation of Vx in memory locations I, I+1, and I+2.
            elif opcode & 0xF0FF == 0xF033:
                logging.debug(hex(opcode) + " == Fx33 - LD B, Vx - Store BCD representation of Vx in memory locations I, I+1, and I+2")
                self.memory[self.I] = (self.V[x >> 8] / 100);
                self.memory[self.I + 1] = ((self.V[x >> 8] / 10) % 10);
                self.memory[self.I + 2] = ((self.V[x >> 8] % 100) % 10);
                self.pc += 2

            # Fx55 - LD [I], Vx - Store registers V0 through Vx in memory starting at location I.
            elif opcode & 0xF0FF == 0xF055:
                logging.debug(hex(opcode) + " == Fx55 - LD [I], Vx - Store registers V0 through Vx in memory starting at location I")
                for i in range(0x10):
                    self.memory[self.I + i] = self.V[i]
                self.pc += 2

            # Fx65 - LD Vx, [I] - Read registers V0 through Vx from memory starting at location I.
            elif opcode & 0xF0FF == 0xF065:
                logging.debug(hex(opcode) + " == Fx65 - LD Vx, [I] - Read registers V0 through Vx from memory starting at location I")
                for i in range(0x10):
                    self.V[i] = self.memory[self.I + i]
                self.pc += 2
        else:
            raise LookupError("This operation is not available, are you using a Super Chip-8 ROM?")

        # Debug logging
        logging.debug("Register I: " + bin(self.I))
        for i in range(0x10):
            logging.debug("Register V[" + hex(i) + "]: " + hex(self.V[i]))
        # logging.debug('\n' + '\n'.join([''.join(['{:2}'.format(int(item)) for item in row])
        #                                for row in self.graphics]))
