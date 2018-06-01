from cpu import Cpu
import os

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
    rom_path = "~Barend/Github/Chip-8/Roms/INVADERS"

    # Load ROM
    load_rom(cpu.memory, cpu.pc, rom_path)

    # Main cycle

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
