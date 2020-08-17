"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # CPU Registers 0 - 7
        self.R = [0] * 8
        # RAM bytes 0 - 255
        self.RAM = [0] * 256
        # Program Counter tells us the RAM address to start
        self.PC = 0

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.RAM[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            #self.fl,
            #self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.R[i], end='')

        print()

    def run(self):
        """Codes for operations"""
        # Register Immediate: Saves value at specified register
        LDI = 0b10000010
        # Print the value at specified register
        PRN = 0b01000111
        # Halt
        HLT = 0b00000001

        """Run the CPU."""
        # Instruction Register. Read the memory address at current PC and save it at IR for reference.
        IR = self.ram_read(self.PC)
        # Save operands of the instruction for reference
        operand_a = self.ram_read(self.PC + 1)
        operand_b = self.ram_read(self.PC + 2)

        
        # Perform a task based on IR
        if IR == LDI:
            self.R[operand_a] = operand_b
            self.PC += 3
        elif IR == PRN:
            print(self.R[operand_a])
            self.PC += 2
        elif IR == HLT:
            exit()
        


    def ram_read(self, MAR):
        # MAR Memory Access Register
        return self.RAM[MAR]

    def ram_write(self, MAR, MDR):
        # MDR Memory Data Register
        self.RAM[MAR] = MDR