## Python Simulator written for iDEA
by Fred and Hui Yan
attached with FYP student Shao Qiu

Original repo: https://github.com/maguire/MIPS-Simulator
(credit to user 'maguire')

### Major Additions and Modifications
* Add support for more instructions
* Read and convert from elf32-bigmips
* Fixed bugs in existing implementation
* Adding preprocessing and data dependency checking
* Basic statistics collecting

### Justification
* An instruction set simulator to model and accurately predict the behavior of instructions' execution.
* Starts with a MIPS model, and will progressively modify according to the iDEA model (https://github.com/brosser/iDEA-Simulator).
* Main motivations:
	- to obtain instruction count.
	- to identify hazards / data dependencies.
	- to ensure logical and functional correctness.
	- to analyse opportunity for composite instructions.
* Cycle-accurate simulator is not needed for now. If the simulator doesn't fulfill the requirements above, then we will move on to a cycle-accurate one. 

### Sections of the Simulator (May change. Not set in stone)
* Assembler
	* Pre-processing tasks: Reads the MIPs asm code generated and grabs the necessary values
	* Analysis: Dependency checks and nop insertions
	* Code optimization: Profiler that checks for opportunities for composite instructions
	* Code generation: Generates the code for simulator, and for IM and DM.
* Simulator
	* Accepts the asm code generated and emulates the execution of the code instructions.
	* Dumps a log file of instruction pipelines.
	
------

### Usage

`python run-simulator.py [options] <Input ASM> <Sim. Log> <Sim. ASM File> <Preproc. Log> <Memory Dump>`

Example:

`python src/run-simulator.py -v benchmark/toy/median/median-O2.asm`

Only the Assembler Input File is a required input, others are optional (default filenames are used).

The input file uses the format elf32-bigmips.

#### Options

- `--version` Show program's version number and exit.
- `-h, --help` Show help message and exit.
- `-v, --verbose` Print cycle by cycle debug information to simulaton log file.
 
#### Output

- `<Simulation Run Log File>` Log file from simulation, showing final register file state, accessed data memory and run statistics
- `<Simulation Assembly File>` The processed Assembly code as input to the simulator
- `<Preprocessing Log File>` Preprocessing logfile, specifying NOP-insertions, branch address recalculations and parse log
- `<Data Memory Dump File>` Pre-simulation data memory dump

#### Automated testing

`./runSimulations.sh`.

Bash script that automatically runs all benchmarks and outputs cycle count.

