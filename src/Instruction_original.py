"""
Instructions to support:

R-Type Instructions [add, sub, and, or, jr, nor, slt]
opcode(6), rs(5), rt(5), rd(5), sa(5), func(6)
I-Type Instructions [addi, subi, ori, bne, beq, lw, sw]
opcode(6), rs(5), rt(5), immediate(16)
J-Type Instructions [j]
opcode(6), target(26)

instr - type of instruction
op - operation
rs - source register
rt - transition register
rd - destination register
sa (shamt) - shift amount
target - target address
func - function
"""

class Instruction(object):
    def __init__(self, **input):
        self.result = None
        
        self.source1RegValue = None 
        self.source2RegValue = None
        self.sourceAddr = None
        self.values = {
                       'op': None,
                       'dest': None,
                       's1': None,
                       's2': None,
                       'immed': None,
                       'shamt': None,
                       'target': None
        }
        self.controls = {'aluop'   : None,
                         'regRead' : None,
                         'regWrite': None,
                         'readMem' : None,
                         'writeMem': None,
                         'branch'  : None  }

        for key in input:
            if key in self.values.keys():
                self.values[key] = input[key]
            else:
                self.controls[key] = input[key]

    @property
    def op(self):
        """ Get this Instruction's name """
        return self.values['op']
    
    @property
    def dest(self):
        """ Get this Instruction's destination register """
        return self.values['dest']
    
    @property
    def s1(self):
        """ Get this Instruction's first source register """
        return self.values['s1']
    
    @property
    def s2(self):
        """ Get this Instruction's second source register """
        return self.values['s2']

    @property
    def shamt(self):
        """ Get this Instruction's shift amount """
        return self.values['shamt']
    
    @property
    def immed(self):
        """ Get this Instruction's immediate value """
        return self.values['immed']
    
    @property
    def target(self):
        """ Get this Instruction's target value """
        return self.values['target']
    
    @property
    def aluop(self):
        """ Get this Instruction's control to decide an alu operation """
        return self.controls['aluop']
    
    @property
    def regRead(self):
        """ Get this Instruction's control to decide to read a register"""
        return self.controls['regRead']
    
    @property
    def regWrite(self):
        """ Get this Instruction's control to decide to write a register """
        return self.controls['regWrite']
    
    @property
    def readMem(self):
        """ Get this Instruction's control to decide to read memory """
        return self.controls['readMem']
    
    @property
    def writeMem(self):
        """ Get this Instruction's control to decide to write memory """
        return self.controls['writeMem']
    
    @property
    def branch(self):
        """ Get this Instruction's control to decide if branch instr """
        return self.controls['branch']
    
    def __str__(self):
        str = "%s\t%s %s %s %s %s %s" % (self.values['op'],
                                  self.values['dest'] if self.values['dest'] else "",
                                  self.values['s1'] if self.values['s1'] else "",
                                  self.values['s2'] if self.values['s2'] else "",
                                  self.values['shamt'] if self.values['shamt'] else "",
                                  self.values['immed'] if self.values['immed'] else "",
                                  self.values['target'] if self.values['target'] else "")
        return str
    
    def __repr__(self):
        return repr(self.values)
        
class Nop(Instruction):
    @property
    def op(self):
        """ Get this Instruction's name """
        return 'nop' 
    def __str__(self):
        return 'nop'  
    pass
    
#nop singleton
Nop = Nop()
