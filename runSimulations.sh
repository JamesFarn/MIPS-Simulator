#Added by James
# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)
# for examples
(set -o igncr) 2>/dev/null && set -o igncr; # this comment is needed
#End added by James

#!/bin/bash

# Bash script to run all toy benchmark simulations
#
# To run this script, do:
#
# $ chmod +x runSimulations.sh
# $ ./runSimulations.sh

# Header
echo -e "\n"
echo -e "Result \t\t\t Benchmark \t\t\t\t Cycles"
echo -e "-----------------------------------------------------------------------"
# Bubble Sort
python src/run-simulator.py -q ./benchmark/toy/bubble_sort/bubble-O0.asm
python src/run-simulator.py -q ./benchmark/toy/bubble_sort/bubble-O0.asm
python src/run-simulator.py -q ./benchmark/toy/bubble_sort/bubble-O1.asm
python src/run-simulator.py -q ./benchmark/toy/bubble_sort/bubble-O2.asm
python src/run-simulator.py -q ./benchmark/toy/bubble_sort/bubble-O3.asm

# Factorial
python src/run-simulator.py -q ./benchmark/toy/factorial/factorial-O0.asm
python src/run-simulator.py -q ./benchmark/toy/factorial/factorial-O1.asm
python src/run-simulator.py -q ./benchmark/toy/factorial/factorial-O2.asm
python src/run-simulator.py -q ./benchmark/toy/factorial/factorial-O3.asm

# Fib
python src/run-simulator.py -q ./benchmark/toy/fib/fib-O0.asm
python src/run-simulator.py -q ./benchmark/toy/fib/fib-O1.asm
python src/run-simulator.py -q ./benchmark/toy/fib/fib-O2.asm
python src/run-simulator.py -q ./benchmark/toy/fib/fib-O3.asm

# Fir
python src/run-simulator.py -q ./benchmark/toy/fir/fir-O0.asm
python src/run-simulator.py -q ./benchmark/toy/fir/fir-O1.asm
python src/run-simulator.py -q ./benchmark/toy/fir/fir-O2.asm
python src/run-simulator.py -q ./benchmark/toy/fir/fir-O3.asm

# Median
python src/run-simulator.py -q ./benchmark/toy/median/median-O0.asm
python src/run-simulator.py -q ./benchmark/toy/median/median-O1.asm
python src/run-simulator.py -q ./benchmark/toy/median/median-O2.asm
python src/run-simulator.py -q ./benchmark/toy/median/median-O3.asm

# MMult
python src/run-simulator.py -q ./benchmark/toy/mmult/mmult-O0.asm
python src/run-simulator.py -q ./benchmark/toy/mmult/mmult-O1.asm
python src/run-simulator.py -q ./benchmark/toy/mmult/mmult-O2.asm
python src/run-simulator.py -q ./benchmark/toy/mmult/mmult-O3.asm

# Negative test (supposed to fail)
python src/run-simulator.py -q ./benchmark/toy/negative/This_test_should_fail.asm

echo -e "\n"
