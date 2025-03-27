import sys

usage = "usage: py VMTranslator filename.vm"

if len(sys.argv) != 3 or sys.argv[2][-3:] is not ".vm":
    sys.exit(usage)

# Handle input file
class Parser:
    def __init__(self, filename):
        self.file = filename
        self.current_command = None
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
    def Constructor(self):
        try:
            open(f"{self.file}", "r")
        except FileNotFoundError:
            sys.exit("Can not open file")

    # Check if whether has the command left
    def hasMoreCommand(self):
        if self.file.readline() = "":
            return False
        return True
    
    # Read the next command from the input and makes it the current command
    def advance(self):
        self.current_command = self.file.readline()

    # Return the type of the command
    def commandType(self):
   

    def arg1(self):
        pass

    def arg2(self):
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