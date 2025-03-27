import sys

usage = "usage: py VMTranslator filename.vm"

if len(sys.argv) != 3 or sys.argv[2][-3:] is not ".vm":
    sys.exit(usage)

# Handle input file
class Parser:

    # Type of command
    C_ARITHMETIC = 1
    C_PUSH = 2
    C_POP = 3
    C_LABEL = 4
    C_GOTO = 5
    C_IF = 6
    C_FUNCTION = 7
    C_RETURN = 8
    C_CALL = 9
    VM_code = ""
    # Open file to read
    def Constructor(self, filename):
        try:
            with open(f"{filename}", "r") as file:
                self.VM_code = file.read()
        except FileNotFoundError:
            sys.exit("Can not open file")

    # Check if whether has the command left
    def hasMoreCommand(self):
        pass
    
    # Read the next command from the input and makes it the current command
    def advance(self):
        pass

    # Return the type of the command
    def commandType(self):
        pass



# Write into output file
class CodeWriter:
    # Create .asm file
    def Constructor(self):
        pass

    # Converting arithemetic VM code to assembly
    def writeArithmetic(self, string):
        pass

    # Converting push & pop operation to assembly
    def writePushPop(self):
        pass

    def close(self):
        pass

def main():
    pass

main()