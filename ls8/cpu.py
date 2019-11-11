"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[7] = 0xF4
        self.pc = 0
        self.MAR = 0
        self.MDR = 0
        self.FL = 0b00000000

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
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "INC":
            self.reg[reg_a] += 1
        elif op == "DEC":
            self.reg[reg_a] -= 1
        elif op == "SUB": 
            self.reg[reg_a] = self.reg[reg_a]-self.reg[reg_b]
        elif op == "MUL": 
            self.reg[reg_a] = self.reg[reg_a]*self.reg[reg_b]
        elif op == "MOD": 
            if self.reg[reg_b]!=0:
                self.reg[reg_a] = self.reg[reg_a]%self.reg[reg_b]
            else:
                raise Exception("can't divide by zero")
        elif op == "ST": 
            self.reg[reg_a] = self.reg[reg_b]
        elif op == "SHL": 
            self.reg[reg_a] = self.reg[reg_a] << self.reg[reg_b]
        elif op == "CMP": 
            if self.reg[reg_a] == self.reg[reg_b]:
                self.FL = 0b00000001
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.FL = 0b00000010
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.FL = 0b00000100

        elif op == "SHR": 
            self.reg[reg_a] = self.reg[reg_a] >> self.reg[reg_b]
        elif op == "XOR": 
            self.reg[reg_a] = self.reg[reg_a] ^ self.reg[reg_a]
        elif op == "OR": 
            self.reg[reg_a] = self.reg[reg_a] | self.reg[reg_a]
        elif op == "NOT": 
            self.reg[reg_a] = ~self.reg[reg_a]
        elif op == "AND": 
            self.reg[reg_a] = self.reg[reg_a] & self.reg[reg_a]
        elif op == "DIV": 
            if self.reg[reg_b]!=0:
                self.reg[reg_a] = self.reg[reg_a]/self.reg[reg_b]
            else:
                raise Exception("can't divide by zero")
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self,address):
        return self.ram[address]
    
    def ram_write(self,address,value):
        self.ram[address] = value

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
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
        opp_dict = {0b0000:'ADD', 0b0001:'SUB', 0b0101:'INC', 0b0110:'DEC', 0b0010:'MUL', 0b0011:'DIV',
                     0b1011:'XOR', 0b0100:'ST', 0b1010:'OR',0b1100:'SHL', 0b1101:'SHR',0b1000 : 'AND',
                     0b0111 :'CMP',0b1001:'NOT'}
        ir = self.ram_read(self.pc)
        operand_a = self.ram_read(self.pc+1)
        operand_b = self.ram_read(self.pc+2)
        if ((ir >>5 ) % (ir >>6)) == 0b1 :  ## USE ALU
            self.alu(opp_dict[ir % (ir<<4)],operand_a,operand_b)
            self.pc += ir >> 6
        elif ir == 0b00000000:
            #NOP
            pass
        elif ir == 0b01010000:
            #TODO CALL
            pass
        elif ir == 0b00000001:
            #TODO HLT
            pass
        elif ir == 0b000010011: 
            #TODO IRET
            pass
        elif ir ==0b01010101:
            #TODO JEQ
            pass
        elif ir ==0b01011010:
            #TODO JGE
            pass
        elif ir == 0b01011001:
            #TODO JLE
            pass
        elif ir == 0b01011000:
            #TODO JLT
            pass
        elif ir == 0b01010100:
            #TODO JMP
            pass
        elif ir == 0b01010110:
            #TODO JNE
            pass
        elif ir == 0b10000011:
            #TODO LD
            pass
        elif ir == 0b10000010:
            #TODO LDI
            pass
        elif ir == 0b01001000:
            #TODO PRA
            pass
        elif ir == 0b01000111:
            #TODO PRN
            pass
        elif ir == 0b01000101:
            #PUSH
            self.reg[7] -=1
            self.ram[self.reg[7]] = operand_a

        elif ir == 0b01000110:
            #POP
            self.reg[operand_a] = self.ram[self.reg[7]]
            self.reg[7] +=1

        elif ir == 0b00010001:
            #TODO RET
            pass
        
        


