"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000
CMP = 0b10100111
JMP = 0b01010100
JNE = 0b01010110
JEQ = 0b01010101

SP = 7
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.reg[SP] = 0xF4
        self.pc = 0
        self.halted = False 
        self.fl = 0b00000000 
        
    def ram_read(self, address):
        '''accept the address to read and return the value stored there'''
        return self.ram[address]

    def ram_write(self, address, val):
        '''accept a value to write, and the address to write it'''
        self.ram[address] = val

    def load(self, filename):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:
        # program = {}
        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]
        # if len(sys.argv) != 2:
        #     print("usage: comp.py progname")
        #     sys.exit(1)
        if len(sys.argv) != 2:
            print('usage: comp.py progname')
            sys.exit(1)

        try:
            with open(filename) as f:
                for line in f:
                    line = line.strip()
                    if line == '' or line[0] == '#':
                        continue
                    try:
                        str_value = line.split('#')[0]
                        value = int(str_value, 2)
                        # self.ram_write(value, address)
                        # address += 1
                    except ValueError:
                        print(f'Invalid number: {str_value}')
                        sys.exit(1)
                    self.ram_write(address, value)
                    address += 1
                    # program[address] = value
                    # address += 1

        except FileNotFoundError:
            print(f'File not found: {sys.argv[1]}')
            sys.exit(2)


        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == 'MUL':
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while not self.halted:
            instruction = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            
            if instruction == HLT:
                self.halted = True
                self.pc += 1

            elif instruction == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3

            elif instruction == PRN:
                print(self.reg[operand_a])
                self.pc += 2

            elif instruction == MUL:
                self.reg[operand_a] *= self.reg[operand_b]
                self.pc += 3

            elif instruction == PUSH:
                self.reg[SP] -= 1
                valueFromRegister = self.reg[operand_a]
                self.ram_write(self.reg[SP], valueFromRegister)
                self.pc += 2

            elif instruction == POP:
                topmostvalue = self.ram_read(self.reg[SP])
                self.reg[operand_a] = topmostvalue
                self.reg[SP] += 1
                self.pc += 2

            elif instruction == CALL:
                value = self.pc + 2
                self.reg[SP] -= 1
                self.ram_write(self.reg[SP], value)
                self.pc = self.reg[operand_a]

            elif instruction == RET:
                self.pc = self.ram_read(self.reg[SP])
                self.reg[SP] += 1
            # print(instruction)
            elif instruction == ADD:
                self.reg[operand_a] += self.reg[operand_b]
                self.pc += 3

            elif instruction == CMP:
                if self.reg[operand_a] == self.reg[operand_b]:
                    self.fl = 0b00000001
                elif self.reg[operand_a] < self.reg[operand_b]:
                    self.fl = 0b00000100
                elif self.reg[operand_a] > self.reg[operand_b]:
                    self.fl = 0b00000010
                self.pc += 3
                # print(self.reg[operand_b])

            elif instruction == JMP:
                self.pc = self.reg[operand_a]

            elif instruction == JEQ:
                if self.fl & 0b1 == 1:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2

            elif instruction == JNE:
                if self.fl & 0b1 == 0:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2

            

