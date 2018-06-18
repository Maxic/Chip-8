from cpu import Cpu
import os
import pygame
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

    # Initialize graphics
    key_lookup = initialize_io()
    key = None

    # Specify Rom (TODO: Build CLI)
    rom_path = "~Barend/Github/Chip-8/Roms/EMULOGO.ch8"

    # Load ROM
    load_rom(cpu.memory, cpu.pc, rom_path)

    # Main cycle
    while cpu.pc <= 4096:
        # Get pressed keys
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                key = key_lookup[event.unicode]

        # fetch opcode from memory
        opcode = cpu.fetch_opcode(cpu.pc)
        hex_opcode = hex(opcode)
        program_counter = cpu.pc

        # Execute opcode
        cpu.execute_operation(opcode, key)


def load_rom(memory, pc, rom_path):
    print("Loading ROM from" + rom_path)
    with open(os.path.expanduser(rom_path), "rb") as f:
        rom_data = f.read()
    i = 0
    while i < len(rom_data):
        memory[pc + i] = rom_data[i]
        i += 1


def initialize_io():
    pygame.init()
    pygame.display.set_mode()
    key_lookup = {
        'q': 0,
        'w': 1,
        'e': 2,
        'a': 3,
        's': 4,
        'd': 5,
        'z': 6,
        'x': 7,
        'c': 8,
        '1': 9,
        '2': 10,
        '3': 11,
        '4': 12,
        '5': 13,
        '6': 14,
        '7': 15,
    }
    return key_lookup


if __name__ == "__main__":
    main()
