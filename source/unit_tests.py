"""
Unit tests for the Pushy Interpreter.
Requires 'pushy_interpreter.py' to be available.
An exit code of 0 means the build is passing. Otherwise, it's failing.
"""

from pushy_interpreter import Script, IO_Util

class DummyIO(IO_Util):
    """ A dummy IO_Util which stores the output rather than printing it.
    Used for verifying output in unit testing. """
    
    def __init__(self, delim = '\n'):
        self.delim = delim
        self.output = ''

    def out(self, *values):
        self.output += ' '.join(str(v) for v in values)
        self.output += self.delim
        self.last_sep = self.delim

def token_test():
    test_cases = [
        #== Format: [script, [<expected tokens>]]
        
        # Check that chars are split:
        ['he1l0', ['h', 'e', '1', 'l', '0']],
        
        # Make sure digits are grouped:
        ['Z99Z9 1010', ['Z', '99', 'Z', '9', ' ', '1010']],
        
        # Ensure leading zeroes are parsed seperately:
        ['015err', ['0', '15', 'e', 'r', 'r']],

        # Make sure special commands 'o?' are parsed:
        ['56 5o/', ['56', ' ', '5', 'o/']],

        # ...but do not interfere with strings:
        ['`Yo`"', ['`', 'Y', 'o', '`', '"']],

    ]

    for test in test_cases:
        assert Script.to_tokens(test[0]) == test[1]

    print("Passed tokenizer test.")

def script_test():
    test_cases = [
        #== Format: [script, [<inputs>], expected output]

        # Hello World
        ['`Hello, World!`"', [], 'Hello, World!\n'],

        # Fibonacci Generator
        ['01{2-:2d+;_', [7], '0 1 1 2 3 5 8\n'],

        # Quine
        ['95 34\n_"\n', [], '95 34\n_"\n'],

        # Sum of factorial's digits
        ['fsS#', [10], '27\n'],

        # Check nested loops
        ['03:3:#', [0], '0\n'*9],
    ]

    for test in test_cases:
        D = DummyIO()
        Script(test[0], D).run(test[1])
        assert D.output == test[2]

    print("Passed basic script test. ")
    
if __name__ == '__main__':
    token_test()
    script_test()
