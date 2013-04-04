#!/usr/bin/python

import elf32parser
import PipelineSimulator
import Instruction
import InstructionParser
import Sourceline
import Checker
from optparse import OptionParser

import os
import sys

def main() :

	verboseFlag = False

	parser = OptionParser(usage="usage: run-simulator.py [-v] filename", version="1.0")
	parser.add_option("-v", "--verbose", 
					action="store_true",
					dest="verboseFlag",
					default=False,
					help="Print cycle by cycle debug information to simulation log file")
	(options, args) = parser.parse_args()

	if len(args) != 1:
		parser.error("Wrong number of arguments")

	# Open the input file
	try:
		inputFile = open(sys.argv[1], "r");
	except IOError:
		print "There was an error opening the input file."
		sys.exit()

	defaultSimASMFile = "simasm.sim"
	defaultDataMemFile = "datamem.sim"
	defaultPreProcLogFile = "preprocLog.sim"
	defaultSimRunFile = "simrun.sim"

	oldstdout = sys.stdout

	# Initialize parsers
	iparser = InstructionParser.InstructionParser()
	eparser = elf32parser.elf32parser()
	
	# Convert elf32-bigmips to simulator friendly format
	SimAsmFileName = sys.argv[3] if len(sys.argv) > 4 else defaultSimASMFile
	SimAsmFile = open(SimAsmFileName, 'w')
	sys.stdout = SimAsmFile

	eparser.convertToSimASM(sys.argv[1], defaultSimASMFile, defaultDataMemFile)
	lines = eparser.getLines()
	datamem = eparser.getDataMem() 
	mainAddr = eparser.getMainAddr()

	# Parse in lines and check for dependencies
	PPLogFileName = sys.argv[3] if len(sys.argv) > 3 else defaultPreProcLogFile
	PPLogFile = open(PPLogFileName, 'w')
	sys.stdout = PPLogFile

	# Get line by line
	lines = iparser.parseLines(lines)

	pipelinesim = PipelineSimulator.PipelineSimulator(lines, datamem, mainAddr, oldstdout, verboseFlag)
	
	print "> Starting Simulation"

	# Set logfile
	simulationFileName = sys.argv[2] if len(sys.argv) > 2 else defaultSimRunFile
	simulationFile = open(simulationFileName, 'w')
	sys.stdout = simulationFile

	# Run simulation
	pipelinesim.run()

	# Print out line by line
	#print lines

	oldstdout.write("\n> Simulation Completed")

	simulationFile.close()
	PPLogFile.close()

	sys.stdout = oldstdout
	checker = Checker.Checker(defaultSimRunFile)
	checker.runCheck()

if __name__ == "__main__":
    main()
