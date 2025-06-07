# Makefile for RPAL Interpreter
# Author: Team TheByteForce
# Student ID: 220303E Kariyawasam U.G.R.T | 220407C: Muthumala. V. D. W

# Main Python script
MAIN = myrpal.py
INPUT = input.txt

# Default: Run the interpreter with just the input file
run:
	python3 $(MAIN) $(INPUT)

# Print the raw contents of the input file
print:
	python3 $(MAIN) -l $(INPUT)

# Generate and print the Abstract Syntax Tree (AST)
ast:
	python3 $(MAIN) -ast $(INPUT)

# Generate and print the Standardized Tree (ST)
st:
	python3 $(MAIN) -st $(INPUT)

# Clean: No real build files in Python, but included for convention
clean:
	rm -rf *.pyc */*.pyc __pycache__ */__pycache__
