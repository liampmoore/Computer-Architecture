"""CPU functionality."""

import sys


"""Codes for operations"""
# Register Immediate: Saves value at specified register
LDI = 0b10000010
# Print the value at specified register
PRN = 0b01000111
# Halt
HLT = 0b00000001
# Multiply
MUL = 0b10100010
# Push
PUSH = 0b01000101
# Pop
POP = 0b01000110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # CPU Registers 0 - 7
        # R5 is reserved as the interrupt mask (IM)
        # R6 is reserved as the interrupt status (IS)
        # R7 is reserved as the stack pointer (SP)
        self.R = [0] * 8
        self.R[7] = 0xF4
    
        # Program Counter tells us the RAM address of current instruction
        self.PC = 0

        # Flags, `00000LGE`, store less, greater, equal of two registers
        self.FL = 0

        # RAM bytes 0 - 255
        self.RAM = [0] * 256

        # Branch table for opcodes
        self.branchtable = {}
        self.branchtable[LDI] = self.handle_LDI
        self.branchtable[PRN] = self.handle_PRN
        self.branchtable[HLT] = self.handle_HLT
        self.branchtable[MUL] = self.handle_MUL
        self.branchtable[PUSH] = self.handle_PUSH
        self.branchtable[POP] = self.handle_POP
    

    def load(self, program):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        for instruction in program:
            self.RAM[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.R[reg_a] += self.R[reg_b]
        elif op == "MUL":
            self.R[reg_a] *= self.R[reg_b]
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

    def advance_PC(self):
        # Use bitshifting to get how many operands you use from the first two values in opcode
        advance_value = self.ram_read(self.PC) >> 6
        advance_value += 1
        self.PC += advance_value

    # Opcode handlers
    def handle_LDI(self):
        # The value at the register specified by PC + 1 is the value at PC + 2
        self.R[self.ram_read(self.PC + 1)] = self.ram_read(self.PC + 2)
        self.advance_PC()

    def handle_PRN(self):
        # Print the value at the register specified by PC + 1
        print(self.R[self.ram_read(self.PC + 1)])
        self.advance_PC()

    def handle_HLT(self):
        # Halt the program, exit the emulator
        exit()

    def handle_MUL(self):
        # Uses the ALU to multiply operands in registers specified by PC + 1 and PC + 2
        self.alu("MUL", self.ram_read(self.PC + 1), self.ram_read(self.PC + 2))
        self.advance_PC()

    def handle_PUSH(self):
        self.R[7] -= 1
        given_register = self.ram_read(self.PC + 1)
        value_in_given_register = self.R[given_register]
        self.ram_write(self.R[7], value_in_given_register)
        self.advance_PC()

    def handle_POP(self):
        SP_value = self.ram_read(self.R[7])
        given_register = self.ram_read(self.PC + 1)
        self.R[given_register] = SP_value
        self.R[7] += 1
        self.advance_PC()


    def run(self):
        """Run the CPU."""
        # Instruction Register. Read the memory address at current PC and save it at IR for reference.
        IR = self.ram_read(self.PC)

        # Perform an operation based on IR
        self.branchtable[IR]()
    

    def ram_read(self, MAR):
        # MAR Memory Access Register
        return self.RAM[MAR]

    def ram_write(self, MAR, MDR):
        # MDR Memory Data Register
        self.RAM[MAR] = MDR