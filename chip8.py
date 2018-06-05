from cpu import Cpu
import os
from pygame import key

"""
+-----------------------+
|   CHIP-8 Emulator     |
|                       |
| Barend Poot      2018 |
+-----------------------+
"""


def main():
    # Initialize CPU
    cpu = Cpu()

    # Specify Rom (TODO: Build CLI)
    rom_path = "~Barend/Github/Chip-8/Roms/UFO"

    # Load ROM
    load_rom(cpu.memory, cpu.pc, rom_path)

    # Initialize graphics
    # something something pygame

    # Main cycle
    while cpu.pc < 4096:
        # Get key pressed
        pressed_key = key.get_pressed()
        opcode = cpu.fetch_opcode(cpu.pc, pressed_key)
        if int(opcode) > 0:
            cpu.execute_operation(opcode)


def load_rom(memory, pc, rom_path):
    print("Loading ROM from %s...", rom_path)
    with open(os.path.expanduser(rom_path), "rb") as f:
        rom_data = f.read()
    i = 0
    while i < len(rom_data):
        memory[pc + i] = rom_data[i]
        i += 1


if __name__ == "__main__":
    main()
