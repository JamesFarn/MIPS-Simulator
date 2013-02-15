# elf32-bigmips to MIPS-Simulator format converter
# Fredrik Brosser 2013-02-15

import sys
import re

class elf32_instr:

	def __init__(self, label, address, opcode, mnemonic, nOperands, operands, indirect):
		self.label = label;
		self.address = address;
		self.opcode = opcode;
		self.mnemonic = mnemonic;
		self.nOperands = nOperands;
		self.operands = operands;
		self.indirect = indirect;
		self.indirectReg = ""
		self.isMemInstr = False

		self.registerList = ['zero', 'at', 'v0', 'v1', 'a0', 'a1' , 'a2', 'a3',
		            't0', 't1', 't2', 't3', 't4', 't5', 't6', 't7',
		            's0', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8',
		            't8' , 't9',
		            'k0', 'k1',
		            'gp', 'sp',
		            's8', 'ra']
		
		self.registerMapping = {'zero':'$r0', 'at':'$r1', 'v0':'$r2', 'v1':'$r3',
					'a0':'$r4', 'a1':'$r5', 'a2':'$r6', 'a3':'$r7',
		            't0':'$r8', 't1':'$r9', 't2':'$r10', 't3':'$r11',
		            't4':'$r12', 't5':'$r13', 't6':'$r14', 't7':'$r15',
		            's0':'$r16', 's1':'$r17', 's2':'$r18', 's3':'$r19', 
		            's4':'$r20', 's5':'$r21', 's6':'$r22', 's7':'$r23', 
		            't8':'$r24' , 't9':'$r25',
		            'k0':'$r26', 'k1':'$r27',
		            'gp':'$r28', 'sp':'$r29',
		            's8':'$r30', 'ra':'$r31'}

		if(mnemonic == "sw" or mnemonic == "lw"):
			self.isMemInstr = True
		else :
			self.isMemInstr = False
		if(indirect is not None):
			self.indirectReg = indirect.translate(None, '()')

	def getData(self):
		labelStr = (self.label + ": ") if self.label is not '' else ""
		printStr = (labelStr + self.address + ":\t" + self.opcode + "\t" + self.mnemonic + "\t")
		for i in range (0, self.nOperands):
			printStr += self.operands[i]
			if(i<self.nOperands-1):
				printStr += ","
		if(self.indirect is not None):
			printStr += self.indirect
		return printStr

	def getSimData(self):
		printStr = (self.mnemonic)
		if(self.nOperands > 0):
			printStr += (" ")
		for i in range (0, self.nOperands):
			if(self.operands[i] in self.registerList):
				printStr += self.registerMapping[self.operands[i]]
			else:
				printStr += self.operands[i]
			if(i<self.nOperands-1):
				printStr += ", "
		if(self.indirect is not None):
			printStr += ("(" + self.registerMapping[self.indirect.strip('()')] + ")")
		return printStr

class elf32_parser:

	def __init__(self):	
		self.inputFile = None
		self.instructions = []

	# Parse instructions from file
	def parseInstructions(self):

		# Read line by line in file, stripping the newline character
		lines = [line.strip() for line in self.inputFile]

		for line in lines:
			# Find assembly instructions (ignoring whitespace lines, C-code and assembler directives)
			# Normal instruction
			match = re.match('([0-9a-fA-F]+)' + ':' + '\s+' + '([0-9a-fA-F]+)' + '\s+' + '(\w+)' + '\s+' + '((\w+)(,\s*-?\w+)*)(\([a-zA-Z0-9_]+\))*', line)
			if match:
				operands = [x.strip() for x in match.group(4).split(',')]
				self.instructions.append(elf32_instr('', match.group(1), match.group(2), match.group(3), len(operands), operands, match.group(7)))
				continue
			# NOPs and instructions without operands
			match = re.match('([0-9a-fA-F]+)' + ':' + '\s+' + '([0-9a-fA-F]+)' + '\s+' + '(\w+)' + '\s?', line)
			if match:
				self.instructions.append(elf32_instr('', match.group(1), match.group(2), match.group(3), 0, [], None))	
		return

	# Convert from elf32-bigmips to simulator friendly format
	def convertToSimASM(self, inputFileName):

		lines = []

		# Open the input file
		try:
		    self.inputFile = open(inputFileName, "r");
		except IOError:
		    print "There was an error opening the input file."
		    sys.exit()

		self.parseInstructions()
		self.inputFile.close()

		for instruction in self.instructions:
			lines.append(instruction.getSimData())

		return lines
