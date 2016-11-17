import sys, ast
from pushy_interpreter import Script

def cmdError(msg):
    raise SystemExit(msg)


# Check whether filename has been provided
if len(sys.argv) < 2:
    cmdError('Usage: pushy <file> [input]')

    
# Check whether specified file exists
try: file = open(sys.argv[1], encoding = 'ASCII')
except FileNotFoundError: cmdError('File error: File not found.')

# Make sure script is in ASCII
try: code = file.read()
except UnicodeDecodeError: cmdError('File error: Pushy files must be ASCII-only.')

# Parse any command-line input
ins = []
if len(sys.argv[2:]) > 0:
    try: ins = ast.literal_eval(' '.join(sys.argv[2:]))
    except: cmdError('Command line error: unable to parse input (should be a valid python literal)')

# Convert input to list type
valid_ins = [list, int, str, tuple]
t = type(ins)

if t not in [list, int, str, tuple]:
    cmdError("Command line error: not an accepted input type.")
elif t == str: ins = [ord(x) for x in ins]
elif t in (list, tuple):
    for x in ins:
        if type(x) != int: cmdError('Command line error: List inputs can only contain integers.')
ins = list(ins)



# === Run Script === #

Script(code).run(*ins)
