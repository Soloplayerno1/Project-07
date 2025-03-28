import sys

usage = "usage: py VMTranslator.py filename.vm"

if len(sys.argv) != 2 or sys.argv[1][-3:] != ".vm":
    print(sys.argv[1][-3:])
    sys.exit(usage)

# Handle input file
class Parser:
    def __init__(self, filename):
        self.file = filename
        self.line = None
        self.current_command = None

    # Open file to read
    def Constructor(self):
        try:
            self.file = open(f"{self.file}", "r")
            return self.file
        except FileNotFoundError:
            sys.exit("Can not open file")

    # Check if whether has the command left
    def hasMoreCommand(self):
        self.line = self.file.readline()
        if self.line == "":
            return False
        return True
    
    # Read the next command from the input and makes it the current command
    def advance(self):
        self.current_command = self.line

    # Return the type of the command
    def commandType(self):
        if self.current_command.startswith("push"):
            return "push"
        if self.current_command.startswith("pop"):
            return "pop"
        if any(self.current_command.startswith(operation) for operation in ["add", "sub", "neg", "eq", "lt", "gt", "and", "or", "not"]):
            return self.current_command.split()[0]

    def arg1(self):
        if any(self.current_command.startswith(operation) for operation in ["add", "sub", "neg", "eq", "lt", "gt", "and", "or", "not"]):
            return self.current_command.split()[0]
        if self.commandType() == "push" or self.commandType() == "pop":
            return self.current_command.split()[1]

    def arg2(self):
        if self.commandType() == "push" or self.commandType() == "pop":
            return self.current_command.split()[2]


# Write into output file
class CodeWriter:
    segment = { 
        "local": 1,
        "argument": 2,
        "this": 3,
        "that": 4,
        "temp": 5,
        "static": 16
    }
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
        string = string.split()
        self.file.write(f"//{string[0]}\n")
        if string[0] == "add":
            self.file.write("@0\nM=M-1\nA=M\nD=M\n@0\nM=M-1\nA=M\nM=D+M\n@0\nM=M+1\n")
        if string[0] == "sub":
            self.file.write("@0\nD=A\nM=M-1\nA=M\nM=D-M\nD=M\n@0\nM=M-1\nA=M\nM=D+M\n@0\nM=M+1\n")
        if string[0] == "neg":
            self.file.write("@0\nD=A\nM=M-1\nA=M\nM=D-M\n@0\nM=M+1\n")
        if string[0] == "eq":
            self.file.write("@0\nM=M-1\nA=M\nD=M\n@0\nM=M-1\nA=M\nM=D-M\n@false\nM;JNE\nM=M+1\n@increase\n0;JMP\n(false)\n@0\nD=A\nA=M\nM=D\n(increase)\n@0\nM=M+1\n")
        if string[0] == "gt":
            self.file.write("@0\nM=M-1\nA=M\nD=M\n@0\nM=M-1\nA=M\nM=D-M\n@gt\nM;JLT\n@0\nD=A\nA=M\nM=D\n@gtstream\n0;jmp\n(gt)\n@1\nD=A\n@0\nA=M\nM=D\n(gtstream)\n@0\nM=M+1\n")
        if string[0] == "lt":
            self.file.write("@0\nM=M-1\nA=M\nD=M\n@0\nM=M-1\nA=M\nM=D-M\n@lt\nM;JGT\n@0\nD=A\nA=M\nM=D\n@ltstream\n0;jmp\n(lt)\n@1\nD=A\n@0\nA=M\nM=D\n(ltstream)\n@0\nM=M+1\n")
        if string[0] == "and":
            self.file.write("@0\nM=M-1\nA=M\nD=M\n@0\nM=M-1\nA=M\nM=D|M\n@0\nM=M+1\n")
        if string[0] == "or":
            self.file.write("@0\nM=M-1\nA=M\nD=M\n@0\nM=M-1\nA=M\nM=D|M\n@0\nM=M+1\n")
        if string[0] == "not":
            self.file.write("@1\nD=A\n@0\nM=M-1\nA=M\nM=D-M")

    # Converting push & pop operation to assembly
    def writePushPop(self, operation, segment, index):
        self.file.write(f"//{operation} {segment} {index}\n")
        if operation == "push":
            if segment == "constant":
                self.file.write(f"@{index}\nD=A\n@0\nA=M\nM=D\n@0\nM=M+1\n")
            else:
                self.file.write(f"@{index}\nD=A\n@{self.segment[segment]}\nD=D+M\nA=D\nD=M\n@0\nA=M\nM=D\n@0\nM=M+1\n")
        if operation == "pop":
            self.file.write(f"@{index}\nD=A\n@{self.segment[segment]}\nD=D+M\n@pop\nM=D\n@0\nM=M-1\nA=M\nD=M\n@pop\nA=M\nM=D\n")

    def close(self, VM_FILE):
        self.file.close()
        VM_FILE.close()

def main():
    parser = Parser(sys.argv[1])
    INPUT_FILE = parser.Constructor()
    writer = CodeWriter(sys.argv[1])
    writer.Constructor()
    while(parser.hasMoreCommand()):
        parser.advance()
        type = parser.commandType()
        arg1 = parser.arg1()
        arg2 = parser.arg2()
        if any(type == operation for operation in ["add", "sub", "neg", "eq", "lt", "gt", "and", "or", "not"]):
            writer.writeArithmetic(arg1)
        if type == "push" or type == "pop":
            writer.writePushPop(type, arg1, arg2)

    writer.close(INPUT_FILE)

main()