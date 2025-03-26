import sys

usage = "usage: py VMTranslator filename.vm"

if len(sys.argv) != 3 or sys.argv[1][-3:] is not ".vm":
    sys.exit(usage)

