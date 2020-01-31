"""CPU functionality."""
import sys

# opcodes
LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
ADD = 0b10100000
RET = 0b00010001
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        # self.reg[7] = 0xF4
        self.reg[7] = 256
        self.sp = self.reg[-1]
        self.pc = 0
        self.fl = 0
        self.ram = [0] * 256
        self.running = True
        self.prn_list = []
        self.branchtable = {LDI: self.ldi,
                            MUL: self.mul,
                            PRN: self.prn,
                            HLT: self.hlt,
                            PUSH: self.push,
                            POP: self.pop,
                            ADD: self.add,
                            CALL: self.call,
                            RET: self.ret,
                            CMP: self.cmp,
                            JMP: self.jmp,
                            JEQ: self.jeq,
                            JNE: self.jne}
        

    def ldi(self, op_a, op_b):
        # Set the value of a register to an integer
        self.reg[op_a] = op_b
        print(f'LDI - Set reg[{op_a}] to {op_b}')
        self.pc += 3

    def prn(self, op_a, op_b):
        # Print value stored in the given register
        print(
            f'PRN - {self.reg[op_a]} is stored in reg[{op_a}]')
        self.pc += 2
        self.prn_list.append(self.reg[op_a])

    def hlt(self, op_a, op_b):
        self.running = False
        print("HLT - Exit the emulator")

    def add(self, op_a, op_b):
        # Add value in two registers and store result in regA
        self.alu('ADD', op_a, op_b)
        # print(
        #     f'ADD - Set reg[{op_a}] to {self.reg[op_a]}+{self.reg[op_b]}')
        # self.reg[op_a] += self.reg[op_b]
        # self.pc += 3

    def mul(self, op_a, op_b):
        # Multiply the values in two registers together
        # and store the result in registerA
        self.alu('MUL', op_a, op_b)
        # print(
        #     f'MUL - Set reg[{op_a}] to {self.reg[op_a]}*{self.reg[op_b]}')
        # self.reg[op_a] *= self.reg[op_b]
        # self.pc += 3
    
    def cmp(self, op_a, op_b):
        # Compare the values in two registers.
        self.alu('CMP', op_a, op_b)
        # If they are equal, set the Equal E flag to 1, otherwise set it to 0.

        # If registerA is less than registerB, set the Less-than L flag to 1, otherwise set it to 0.

        # If registerA is greater than registerB, set the Greater-than G flag to 1, otherwise set it to 0.

    def jmp(self, op_a, op_b):
        # Jump to the address stored in the given register
        print(f'JUMP to address {self.reg[op_a]}')
        # Set PC to address stored in given register
        self.pc = self.reg[op_a]

    def jeq(self, op_a, op_b):
        # If equal flag is set (true),
        if self.E == 1:
            # jump to the address stored in the given register.
            print(f'JEQ - E flag is set, jumping to address {self.reg[op_a]}')
            # Set PC to address stored in given register
            self.pc = self.reg[op_a]
        else:
            print('JEQ - E flag is clear, not jumping.')
            self.pc += 2

    def jne(self, op_a, op_b):
        # If E flag is clear (false, 0), 
        if self.E == 0:
            # jump to the address stored in given register.
            print(f'JNE - E flag is clear, jumping to address {self.reg[op_a]}')
            # Set PC to address stored in given register
            self.pc = self.reg[op_a]
        else:
            print('JNE - E flag is set, not jumping.')
            self.pc += 2

    def push(self, op_a, op_b):
        # Push value in the given register to stack
        val = self.reg[op_a]
        print(f'PUSH - {val} in reg[{op_a}] to {self.sp}')
        # Decrement SP
        self.sp -= 1
        # Copy value in registers to address by SP
        self.ram[self.sp] = val
        self.pc += 2

    def pop(self, op_a, op_b):
        # Pop value from top of stack to register
        # Copy value from address by SP to register
        val = self.ram[self.sp]
        print(f'POP - {val} from {self.sp} to reg[{op_a}]')
        self.reg[op_a] = val
        # Increment SP
        self.sp += 1
        self.pc += 2

    def call(self, op_a, op_b):
        # Calls subroutine at address stored in the register
        # Address of instruction after CALL pushed to stack
        # self.push(op_a, op_b)
        self.sp -= 1
        self.ram[self.sp] = self.pc + 2
        # PC set to address stored in given register
        subroutine_address = self.reg[op_a]
        print(f'CALL - SR at address {subroutine_address}')
        # Jump to loc in RAM and run 1st IR in subroutine
        # PC can move forward/backwards from current location
        self.pc = subroutine_address

    def ret(self, op_a, op_b):
        # Return from subroutine
        # Pop value from top of stack and store in PC
        self.pc = self.ram[self.sp]
        print(f'Returning to address {self.pc}')
        # Increment SP by 1
        self.sp += 1

    def load(self, filename):
        """Load a program into memory."""
        try:
            address = 0
            with open(filename) as f:
                print(f"Opening file: {filename}")
                for line in f:
                    # Remove comments
                    comment_split = line.split('#')
                    num = comment_split[0].strip()
                    # Skip blank lines
                    if num == '':
                        continue
                    # Convert ls-8 to base 2
                    value = int(num, 2)
                    self.ram_write(address, value)
                    address += 1

        except FileNotFoundError:
            print(f'{sys.argv[0]}: {filename} not found')
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            print(
                f'ADD - Set reg[{reg_a}] to {self.reg[reg_a]}+{self.reg[reg_b]}')
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            print(
                f'MUL - Set reg[{reg_a}] to {self.reg[reg_a]}*{self.reg[reg_b]}')
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == 'CMP':
            if self.reg[reg_a] == self.reg[reg_b]:
                print(f'CMP - Equal flag is set (True, 1) [{self.reg[reg_a]} = {self.reg[reg_b]}]')
                self.E = 1
            else:
                print(f'CMP - Equal flag is clear (False, 0) [{self.reg[reg_a]} != {self.reg[reg_b]}]')
                self.E = 0
            if self.reg[reg_a] < self.reg[reg_b]:
                self.L = 1
            else:
                self.L = 0
            if self.reg[reg_a] > self.reg[reg_b]:
                self.G = 1
            else:
                self.G = 0
        else:
            raise Exception("Unsupported ALU operation")
        self.pc += 3

    def trace(self):
        """
        Handy function to print out the CPU state. 
        You might want to call this from run() 
        if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        count = 1
        while self.running:
            # Instruction Register - current instruction
            ir = self.ram[self.pc]
            print(f'Step {count}:')
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            try:
                self.branchtable[ir](operand_a, operand_b)
            except KeyError:
                print(f"Error: Unknown command: {ir}")
                sys.exit(1)
            count += 1
        print(self.prn_list)

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, address, mdr):
        self.ram[address] = mdr
