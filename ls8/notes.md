## Inventory
- asm: creates a ls8 binary file from our assembly language
- examples: example ls8 files
- readme: containts step by step instructions for the project
- cheatsheet: contains binary instructions for various operations
- spec: the source of truth for the ls8 specifications
- ls8: the main python file to boot up the emulated computer
- cpu: the file that contains our cpu class, the hardware

## What is the ls8?
- It's an 8-bit computer with 8-bit memory addressing
- One byte = 8-bits = 8 "0" or "1"
- 8-bit CPU means 8 registers to work on, 0-7
- With 8-bit memory addressing, there are 256 distinct bytes of memory


### Step 1
- Add list properties to CPU class
- 8 registers R = [0] * 8  
- 256 bytes of RAM RAM = [0] * 256
- Also, PC, IR, MAR, MDR, FL

### Step 2
- Add methods to class
- ram_read(MAR)
- ram_write(MDR, MAR) 

### Step 3
- run()
- Reads PC program counter
- Store that in IR instruction register
- Using ram_read get the bytes at addresses PC+1 and PC+2 from ram, as operand_a and operand_b
- if else cascade for instructions
- After any operation, PC needs to at the next instruction for next loop
- Number of bytes an instruction uses is determined by 6-7 of the instruction opcode
- At the beginning of each instruction, `AABCDDDD`,  Num operands 0-2, 1 if an ALU operation, 1 if instruction sets the PC, Instruction identifier
### Step 4
- Add HLT handler in run
- Breaks the loop and exits no matter how many more instructions there are
### Step 5
- LDI handler
- Sets a specific register to a specified value
### Step 6
- PRN handler
- Prints decimal value to console

### Goal for Day 1
- Print the value 8