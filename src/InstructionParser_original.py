from Instruction import Instruction
from Instruction import Nop

class InstructionParser(object):

    def __init__(self):

        self.expandInstruction = False
        self.instructionSet = {
            'pseudo': ['neg', 'negu', 'abs', 'break'],
            'rtype': ['add', 'sub', 'and', 'or', 'jr', 'jalr', 'nor', 'slt',
                      'addu', 'subu', 'sltu', 'xor',
                      'sll', 'srl', 'sra', 'sllv', 'srlv', 'srav',
                      'jr', 'nop', 'mult', 'multu', 'div', 'divu',
                    'mflo', 'mfhi', 'mtlo', 'mthi'],
            'itype': ['addi', 'subi', 'ori', 'lw', 'sw', 'lh', 'lb', 'sh', 'sb', 'lhu', 'lbu', 'shu', 'sbu',
                        'addiu', 'slti', 'sltiu', 'andi', 'xori', 'lui', 'li',
                        'bne', 'beq', 'blez', 'bgtz', 'bltz', 'bgez', 'bnez', 'beqz',
                        'move'],
            'jtype': ['j', 'jal']
        }

        self.loglines = { 
            "MEM": "Memory dependency between instructions at memory locations ",
            "WAR": "WAR dependency between instructions at memory locations ",
            "RAW": "RAW dependency between instructions at memory locations ",
            "WAW": "WAW dependency between instructions at memory locations ",
            "END": "End of logfile"
            }

        self.nopInserts = []
        self.nNOPs = 0

    def parseFile(self, filename):
        with open(filename) as f:
            data = filter((lambda x: x != '\n'), f.readlines())
            
            instructions = [self.parse(a.replace(',',' ')) for a in data]
            return instructions

    def parseLines(self, lines):
        print "###################### Preprocessing Logfile ######################\n"
        instructions = [self.parse(a.replace(',',' ')) for a in lines]
        instructions = self.createEndInstruction(instructions)
        print "<Successfully parsed instructions>"
        print "\tInstruction Count: ", len(instructions) 
        instructions = self.checkDependencies(instructions)
        print "\n<Preprocessing finished>"
        return instructions

    def parse(self, s):
        s = s.split()
        
        instr = s[0]
        instr.strip()
        
        if instr in self.instructionSet['pseudo']:
            return self.translatePseudoInstruction(s)
        if instr in self.instructionSet['rtype']:
            return self.createRTypeInstruction(s)
        elif instr in self.instructionSet['itype']:
            return self.createITypeInstruction(s)    
        elif instr in self.instructionSet['jtype']:
            return self.createJTypeInstruction(s)
        else:
            print "Could not parse instruction: ", instr
            raise ParseError("Invalid parse instruction")

##########################################################
#
#   INSTRUCTION CREATION
#
##########################################################

    def translatePseudoInstruction(self, s):
        if(s[0] in ["neg", "negu"]):
            return Instruction(op="sub", dest=s[1], s1=s[2], s2="$0", regRead=1, regWrite=1, aluop=1)
        elif s[0] == "abs" and n == 0:
            return Instruction(op="abs", s1 = s[1], regRead = 1, regWrite=1, aluop=1)
        elif s[0] == "break":
            return Nop

    def createEndInstruction(self, instructions):
        replaceindex = -1
        for idx, instr in enumerate(reversed(instructions)):
            if instr.op == 'jr':
                replaceindex = len(instructions)-idx
                break
        if(replaceindex != -1):
            instructions.pop(replaceindex-1)
            instructions.insert(replaceindex, Instruction(op="END", dest=None, s1=None, s2=None, regRead=0, regWrite=0, aluop=0))
        return instructions

    #TODO should be figuring out controls dynamically based on the op
    def createRTypeInstruction(self, s):
        if s[0] in ["jr", "jalr"]:
            return Instruction(op=s[0], s1 = s[1], regRead = 1, aluop=0, branch=1)
        if(s[0] == "nop" or (s[0] == "sll" and s[1] == "$r0")):
            return Nop
        if(s[0] in ["mult", "multu"]):
            return Instruction(op=s[0], dest=s[1], s1=s[1], s2=s[2], regRead=1, regWrite=1, aluop=1)
        if(s[0] in ["mflo", "mfhi"]):
            return Instruction(op=s[0], dest=s[1], s1=None, s2=None, regWrite=1, aluop=1)
        if(s[0] in ["mtlo", "mthi"]):
            return Instruction(op=s[0], dest=s[1], s1=None, s2=None, regWrite=1, aluop=1)
        if(s[0] in ['sll', 'srl', 'sra']):
            return Instruction(op=s[0], dest=s[1], s1=s[2], shamt=s[3], regRead=1, regWrite=1, aluop=1)
        return Instruction(op=s[0], dest=s[1], s1=s[2], s2=s[3], regRead=1, regWrite=1, aluop=1)

    def createITypeInstruction(self, s):
        memread = s[0] in ['lw', 'lb', 'lh', 'lbu', 'lhu']
        memwrite = s[0] in ['sw', 'sb', 'sh', 'sbu', 'shu']
        if (memread or memwrite):
            import re 
            #regex = re.compile("(\d+)\((\$r\d+)\)")
            regex = re.compile("(-?\d+)\((\$r\d+)\)")
            match = regex.match(s[2])
            immedval = match.group(1) 
            sval = match.group(2)
            if s[0] in ['lw', 'lb', 'lh', 'lbu', 'lhu'] :
                return Instruction(op=s[0], dest = s[1], s1=sval, immed = immedval, regRead = 1,regWrite = 1, aluop=1,  readMem = 1)
            else:
                return Instruction(op=s[0],  s1 = s[1], s2=sval,immed = immedval, regRead = 1, aluop=1, writeMem = 1)
        elif ( s[0] in ['bne', 'beq'] ) :
            return Instruction(op=s[0], s1=s[1] , s2= s[2], immed = s[3], regRead = 1, aluop = 1, branch=1)
        elif( s[0] in ['beqz', 'bnez', 'blez', 'bgtz', 'bltz', 'bgez'] ) :
            return Instruction(op=s[0], s1=s[1], s2 = None, immed=s[2], regRead = 1, aluop = 1, branch=1)

                                                        # HEX
            #return Instruction(op=s[0], s1=s[1], immed= int(str(s[2]), 16), regRead = 1, aluop = 1, branch=1)
        # Pseudoinstructions
        if( s[0] == "move" ) :
            return Instruction(op="addi", dest=s[1], s1=s[2], immed=0, regRead=1, regWrite=1, aluop=1)
        elif( s[0] in ["li", "lui"]) :
            return Instruction(op=s[0], dest=s[1], s1=s[2], immed=s[2], regRead=0, regWrite=1, aluop=1)
        else :
            return Instruction(op=s[0], dest=s[1], s1=s[2], immed=s[3], regRead=1, regWrite=1, aluop=1)

    def createJTypeInstruction(self, s):
        # J or JAL
        return Instruction(op=s[0], target=s[1], branch=1)


##########################################################
#
#   DEPENDENCY CHECKING
#
##########################################################

    # Checking for WAR, RAW and Memory depencences between consecutive instructions
    def checkDependencies(self, instructions):
        print "\n<Dependency Checking>"
        if(self.nNOPs == 0):
            print "\tDependency Check = OFF\n\tInserted 0 NOPs"
            return instructions
        print "<Unprocessed Instructions>"
        addr = 0x0
        for i in instructions:
            print hex(addr), ": ", i
            addr += 0x4

        print "\n<Data Dependencies>"
        for i in range(0, len(instructions)-2):
            current = instructions[i]
            next = instructions[i+1]
            
            # Check memory dependencies
            # If writing to a memory location being written to or read in the next instruction
            if(current.writeMem) :
                if(next.writeMem and (current.s2 == next.s2) and 
                        (abs(int(current.immed) - int(next.immed)) <= 4)) :
                    self.addDep(i+1, "MEM")
                if(next.readMem and (current.s2 == next.s1) and 
                        (abs(int(current.immed) - int(next.immed)) <= 4)) :
                    self.addDep(i+1, "MEM")
            if(current.dest == next.s1 or current.dest == next.s2) :
                self.addDep(i+1, "RAW")
            if(next.dest == current.s1 or next.dest == current.s2) :
                self.addDep(i+1, "WAR")
            if(next.dest == current.dest) :
                self.addDep(i+1, "WAW")
        return self.insertNOPs(instructions)

    # Insert NOPs
    def insertNOPs(self, instructions):
        for k in range(0, len(self.nopInserts)):
            instructions.insert(self.nopInserts[k], Nop)
            # Recalculate target values for branches and jumps
            for i in instructions:
                targetval = 0
                vstr = ''
                if i.branch:
                    if(i.op in ['bne', 'beq', 'blez', 'bgtz', 'bltz' 'bgez', 'bnez']) :
                        targetval = int(i.immed)
                        vstr = 'immed'
                    elif(i.op == 'j'):
                        targetval = int(i.target)
                        vstr = 'target'
                    else:
                        targetval = 0
                if(targetval >= (self.nopInserts[k])*4):
                    targetval += 4
                    i.values[vstr] = targetval
                
            for j in range(k+1, len(self.nopInserts)):
                self.nopInserts[j] += 1

        print "\n<Processed Instructions>"
        addr = 0x0
        for i in instructions:
            print hex(addr), ": ", i
            addr += 0x4

        return instructions

    def addDep(self, i, logstr):
        print (self.loglines[logstr] + hex(4*(i+1)) + " and " + hex(4*(i+2)))
        if(i not in self.nopInserts) :
            print "Inserting ", self.nNOPs, " NOP(s)"
            for k in range(0, self.nNOPs):
                self.nopInserts.append(i)
        return

##########################################################
#
#   ERROR CLASS
#
##########################################################

class ParseError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
