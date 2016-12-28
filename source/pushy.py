"""
Command line interface for Pushy.
Requires pushy_interpreter.py to be available.
"""

import ast
import sys

USAGE = """Usage:
  $ pushy t <script-text> [input]
  $ pushy f <script-file> [input]"""

def error(text):
    raise SystemExit(text)

try:
    import pushy_interpreter
except:
    error("Error: Could not import 'pushy_interpreter'.")

def parse_args():
    args = sys.argv[1:]

    if len(args) < 2:
        error(USAGE)

    scripttype = args[0].lower()
    if scripttype not in ('t', 'f'):
        error(USAGE)

    if scripttype == 't':
        script = args[1]
    elif scripttype == 'f':
        try:
            script = open(args[1]).read()
        except:
            error("Could not find file '{0}'.".format(args[1]))

    if len(args) == 2:
        return (script, [])

    return (script, safe_eval(args[2]))

def safe_eval(text):
    try:
        literal = ast.literal_eval(text)
    except:
        error("Could not parse input. Please provide a valid Python literal.")

    allowed_types = [int, list, tuple, str]

    if type(literal) in (tuple, list):
        for item in literal:
            if type(item) != int:
                error("Inputs lists must only contain integers. ")
        return literal

    elif type(literal) == int:
        return [literal]

    elif type(literal) == str:
        return [ord(char) for char in literal]

    else:
        error("Not a valid input type.")


if __name__ == '__main__':

    args = parse_args()
    try:
        pushy_interpreter.Script(args[0]).run(args[1])
    except KeyboardInterrupt:
        error("Program terminated (keyboard interruption).")
    except Exception as e:
        error("Python error: " + repr(e))
