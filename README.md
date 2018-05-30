# Chip-8

    +-----------------------+
    |   CHIP-8 Emulator     |
    |                       |
    | Barend Poot      2018 |
    +-----------------------+

    Memory Map: 4096 bytes
    +---------------+= 0xFFF (4095) End of Chip-8 RAM
    |               |
    |               |
    |               |
    |               |
    |               |
    | 0x200 to 0xFFF|
    |     Chip-8    |
    | Program / Data|
    |     Space     |
    |               |
    |               |
    |               |
    +- - - - - - - -+= 0x600 (1536) Start of ETI 660 Chip-8 programs
    |               |
    |               |
    |               |
    +---------------+= 0x200 (512) Start of most Chip-8 programs
    | 0x000 to 0x1FF|
    | Reserved for  |
    |  interpreter  |
    +---------------+= 0x000 (0) Start of Chip-8 RAM

    Register map
    +---|-------------------|-----------------------+            
    16  | 8-bit registers   | Vx                    |
    1   | 16-bit register   | I                     |
    1   | 8-bit register    | delay                 |
    1   | 8-bit register    | sound                 |
    1   | 16-bit register   | program counter (pc)  |
    1   | 8-bit register    | stack pointer (sp)    |
    16  | 16-bit register   | stack                 |
    +---|-------------------|-----------------------|

    Instructions

    An instruction consists of 2 bytes (16 bits). Some variables are defined here:

    0000 0000 0000 0000
         +------------+ nnn or addr - A 12-bit value, the lowest 12 bits of the instruction
              +-------+ kk or byte - An 8-bit value, the lowest 8 bits of the instruction
                   +--+ n or nibble - A 4-bit value, the lowest 4 bits of the instruction
         +--+           x - A 4-bit value, the lower 4 bits of the high byte of the instruction 
              +--+      y - A 4-bit value, the upper 4 bits of the low byte of the instruction 


Sources:
- http://www.multigesture.net/articles/how-to-write-an-emulator-chip-8-interpreter/
- http://devernay.free.fr/hacks/chip8/C8TECH10.HTM
- http://www.emulator101.com/introduction-to-chip-8.html
- http://mattmik.com/files/chip8/mastering/chip8.html
