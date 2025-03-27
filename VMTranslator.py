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

    # Open file to read
    def Constructor(self):
        try:
            open(f"{self.file}", "r")
        except FileNotFoundError:
            sys.exit("Can not open file")

    # Check if whether has the command left
    def hasMoreCommand(self):
        if self.file.readline() == "":
            return False
        return True
    
    # Read the next command from the input and makes it the current command
    def advance(self):
        self.current_command = self.file.readline().split()

    # Return the type of the command
    def commandType(self):
        if self.current_command.startwith("push"):
            return self.C_PUSH
        if self.current_command.startwith("pop"):
            return self.C_POP
        return self.C_ARITHMETIC

    def arg1(self):
        if self.commandType() is self.C_ARITHMETIC:
            return self.current_command[0]
        return self.current_command[1]

    def arg2(self):
        if self.commandType() is not self.C_ARITHMETIC:
            return self.current_command[2]


# Write into output file
class CodeWriter:
    # Create .asm file
    def __init__(self, filename):
        self.filename = filename.replace(".vm", ".asm")
        self.file = None

    def Constructor(self):
        try:
            self.file = open(f"{self.filename}", "a")
        except FileExistsError:
            sys.exit(f"{self.file} has already exit")

    # Converting arithemetic VM code to assembly
    def writeArithmetic(self, string):
        self.file.write(f"{string[0]}")
        if string[0] == "add":
            self.file.write(f"@0\nM=M-1\nA=M\nD=M\n@0\nM=M-1\nA=M\nM=D+M\n@0\nM=M+1\n")
            

    # Converting push & pop operation to assembly
    def writePushPop(self):
        pass

    def close(self):
        pass

def main():
    pass

main()