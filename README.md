# RPAL-Interpreter
An interpreter for the functional programming language RPAL, built with a scanner, parser, and a Control Stack Evaluation (CSE) machine. It processes RPAL source code by tokenizing input, parsing it into an abstract syntax tree (AST), and evaluating expressions using the CSE model.

Features:
  - Lexical analysis (tokenization of RPAL code)
  - AST generation
  - Tree standardization
  - Evaluation via Control Stack Evaluation (CSE) machine
  - Command-line interface for full control

Project_structure:
  - path: RPAL-Interpreter/
    contents: 
      - myrpal.py: Main runner script
      - src/:
      - Test
      - Validators
      - Input

run_instructions:
  note: >
  
    Make sure to include your RPAL input file (e.g., `input.txt`) inside the `/RPAL-Interpreter` directory.

  command_format: "python3 ./myrpal.py [-l] [-ast] [-st] filename"
  usage_details:
  
    - description: Basic usage without any flags
      command: python3 ./myrpal.py input.txt
      behavior: Evaluates the RPAL program using the CSE machine and prints the result

    - description: Print raw source code from the file
      command: python3 ./myrpal.py -l input.txt

    - description: Display the Abstract Syntax Tree (AST)
      command: python3 ./myrpal.py -ast input.txt

    - description: Display both AST and Standardized Tree (ST)
      command: python3 ./myrpal.py -ast -st input.txt

    - description: Display only the Standardized Tree (ST)
      command: python3 ./myrpal.py -st input.txt

  flags:
  
    - flag: -l
      description: Outputs the source code from the file

    - flag: -ast
      description: Generates and prints the Abstract Syntax Tree

    - flag: -st
      description: Generates and prints the Standardized Tree

    - flag_combo: -ast -st
      description: Prints AST first, then the Standardized Tree

notes:
  - .pyc files are compiled Python bytecode. They are auto-generated and can be safely deleted.

requirements:
  - Python 3.13
  - No third-party libraries required
