"""
Pushy Interpreter - Version 2 (rewrite)
Created 26/12/16
"""

import math
import operator
import random
import re
import string
import sys
import time

class Stack(list):
    """ A basic LIFO (last in = first out) integer stack, with utility functions. """

    def __init__(self, *values):
        self.push(*values)

    def push(self, *values):
        """ Push a list of integer values to the stack (in the given order). """
        for v in values:
            if type(v) in (int, float, bool):
                super().append(int(v))

    # Alias "append" with "push", like regular Python lists.
    append = push

    def pop(self, index = -1, peek = False):
        """ Pop a stack item at the given index.
        Returns None in the case of an invalid index.
        The `peek` parameter suppresses popping if True. """

        if not self.has_index(index):
            return None

        if peek:
            return self[index]

        else:
            return super().pop(index)

    def has_index(self, index):
        """ Checks whether the given index exists in the stack. """

        length = len(self)

        # Return False for empty stack.
        if length < 1:
            return False

        # Strip decimal places if `index` is a float.
        if isinstance(index, float):
            index = int(index)

        # Return False for non-integer indexes.
        if not isinstance(index, int):
            return False

        # Due to Python's negative indexes, all values N in
        # -length <= N < length
        # are valid list indexes in a non-empty list.
        return -length <= index < length

    def clear(self):
        """ Clears the stack, returning all deleted values. """
        data = self.copy()
        del self[:]
        return data

    def run_unary(self, func, on_all = False):
        """ Run a unary function which maps an integer to a new value.
        This can be done "on_all" items (in place), or the last. """
        if len(self) < 1:
            return

        if not on_all:
            self.push(func(self.pop()))
            return

        for i in range(len(self)):
            self[i] = int(func(self[i]))

""" Define loop classes to be in the interpreter. """

class Loop:
    def __init__(self, env):
        pass

    def verify(self, env):
        pass

class ForLoop(Loop):
    def __init__(self, env):
        stack = env.curr_stack()

        if len(stack) < 1:
            self.iters = 0

        else:
            self.iters = stack.pop()

    def verify(self, env):
        if self.iters > 0:
            self.iters -= 1
            return True

        return False

class WhileLoop(Loop):
    def verify(self, env):
        val = env.curr_stack().pop(peek = True)

        if val == None:
            return False

        if val == 0:
            return False

        return True

class IfStatement(Loop):
    def __init__(self, env):
        val = env.curr_stack().pop()

        if val == None:
            self.valid = False

        if val == 0:
            self.valid = False

        else:
            self.valid = True

    def verify(self, env):
        if self.valid:
            self.valid = False
            return True

        return False

class InfLoop(Loop):
    def verify(self, env):
        return True

""" Define all commands to be used in the interpreter. """

def all_equal(env, stack):
    val = stack.pop(peek = True)
    for x in stack:
        if x != val:
            stack.push(0)
            return
    stack.push(1)

def binary_digits(x):
    x = abs(x)

    result = []
    while x > 0:
        result.append(x%2)
        x >>= 1

    return result[::-1]

def clear_stack(env, stack):
    stack.clear()

def ConstNilad(*value):
    def stack_func(env, stack):
        stack.push(*value)
    return (stack_func, 0)

def copy_input(env, stack):
    stack.push(*env.inputs)

def copy_region(env, stack):
    val = stack.pop()
    stack.push(*stack[-val:])

def copy_to_out(env, stack):
    env.OUT.clear()
    env.OUT.push(*env.IN.copy())

def digit_length(x):
    return len(str(abs(x)))

def dupe_last(env, stack):
    stack.push(stack.pop(peek = True))

def e_notation(x, y):
    return x * (pow(10, y))

def factorial(x):
    return math.factorial(abs(x))

def get_random(env, stack):
    values = (stack.pop(), stack.pop())
    stack.push(random.randint(min(values), max(values)))

def goto_in(env, stack):
    env.focus = True

def goto_out(env, stack):
    env.focus = False

def head(x):
    return x + 1

def interrupt(env, stack):
    # Exit with exit code of last stack item.

    val = stack.pop(peek = True)
    if val == None:
        val = 0

    quit(val)

# Integer root of N: the largest whole number, x, where x^2 <= N
def intsqrt(n):
    if n < 1: return n
    x = n
    while True:
        y = (n//x+x)//2
        if x <= y: return x
        x = y

def ispalindrome(x):
    s = str(x)
    return s == s[::-1]

def is_set(env, stack):
    stack.push(len(set(stack)) == len(stack))

def is_sorted_asc(env, stack):
    b = all(stack[i] <= stack[i+1] for i in range(len(stack)-1))
    stack.push(b)

def is_sorted_desc(env, stack):
    b = all(stack[i] >= stack[i+1] for i in range(len(stack)-1))
    stack.push(b)

def join_ints(env, stack):
    if len(stack) < 2:
        return

    s = ''

    if env.on_all:
        values = stack.clear()
        s = str(values[0])
        s += ''.join(str(abs(x)) for x in values[1:])

    else:
        n1, n2 = stack.pop(), stack.pop()
        s = str(n2) + str(abs(n1))

    stack.push(int(s))

def lcm(a, b):
    return (a * b) // math.gcd(a, b)

def leftshift(env, stack):
    stack.push(stack.pop(index = 0))

#TODO: unspaghetti this mess
def MathFunc(operation, fail = 0):
    def stack_func(env, stack):
        if not env.on_all:
            if len(stack) < 2:
                return

        val = stack.pop()
        def unary_func(x):
            try:
                return int(operation(x, val))
            except:
                return fail
        stack.run_unary(unary_func, on_all = env.on_all)
    return (stack_func, 1)

def mirror(env, stack):
    data = stack.copy()[:-1]
    stack.push(*data[::-1])

def multiple_copies(env, stack):
    copies = stack.pop()
    value = stack.pop(peek = True)
    for i in range(copies):
        stack.push(value)

def multiply_stack(env, stack):
    val = stack.pop()
    data = stack.clear()
    data *= val
    stack.push(*data)

def no_delim(env, stack):
    env.io.set_delim('')

def not_bool(x):
    return int(x == 0)

def op_on_all(env, stack):
    env.on_all = True

def op_on_last(env, stack):
    env.on_all = False

def out_lowercase(env, stack):
    env.io.out(''.join(chr(97 + i%26) for i in stack))

def out_uppercase(env, stack):
    env.io.out(''.join(chr(65 + i%26) for i in stack))

def pop_first(env, stack):
    stack.pop(index = 0)

def pop_last(env, stack):
    stack.pop()

def primality(n):
    """ Check the primality of an integer. Returns True or False. """
    
    if n < 2:
        return False

    if n < 4:
        return True

    if n % 2 == 0:
        return False

    if n % 3 == 0:
        return False

    root = math.sqrt(n)

    f = 5
    while f <= root:
        if n%f == 0:
            return False
        if n%(f+2) == 0:
            return False
        f += 6

    return True

def prime_filter(env, stack):
    data = stack.clear()
    data = filter(primality, data)
    stack.push(*data)

def print_char(env, stack):
    val = stack.pop(peek = True)
    if val > 0:
        env.io.out(chr(val))

def print_charcodes(env, stack):
    s = ''
    for i in stack:
        if i > 0:
            s += chr(i)
    env.io.out(s)

def print_int(env, stack):
    env.io.out(stack.pop(peek = True))

def print_stack(env, stack):
    env.io.out(*stack)

def product(env, stack):
    prod = 1
    for val in stack:
        prod *= val

    stack.push(prod)

def push_inc_range(env, stack):
    val = stack.pop()
    if val == 0:
        return

    elif val < 0:
        stack.push(*range(val, 0))

    else:
        stack.push(*range(1, val+1))

def push_range(env, stack):
    val = stack.pop()
    if val == 0:
        return

    elif val < 0:
        stack.push(*range(val+1, 1))

    else:
        stack.push(*range(val))


def rightshift(env, stack):
    stack.insert(0, stack.pop())

def reverse_stack(env, stack):
    data = stack.clear()
    stack.push(*reversed(data))

def send_to_in(env, stack):
    val = env.OUT.pop()
    if val != None:
        env.IN.push(val)

def send_to_out(env, stack):
    val = env.IN.pop()
    if val != None:
        env.OUT.push(val)

def set_delim(env, stack):
    val = abs(stack.pop())
    env.io.set_delim(chr(val))

def shuffle_stack(env, stack):
    data = stack.clear()
    random.shuffle(data)
    stack.push(*data)

def sort_asc(env, stack):
    data = stack.clear()
    stack.push(*sorted(data))

def sort_desc(env, stack):
    data = stack.clear()
    stack.push(*sorted(data, reverse = True))

def split_int(env, stack):
    item = abs(stack.pop())
    digits = map(int, str(item))
    stack.push(*digits)

def stack_equality(env, stack):
    stack.push(int(env.IN == env.OUT))

def stack_ispalindrome(env, stack):
    stack.push(stack == stack[::-1])

def stack_len(env, stack):
    stack.push(len(stack))

def sum_stack(env, stack):
    stack.push(sum(stack))

def swap_stacks(env, stack):
    env.swap_stacks()

def tail(x):
    return x - 1

def ternary(env, stack):
    a = stack.pop()
    tVal = stack.pop()
    fVal = stack.pop()
    stack.push(tVal if a else fVal)

def tobinary(env, stack):
    val = stack.pop()
    stack.push(*binary_digits(val))

def UnaryFunc(func):
    def stack_func(env, stack):
        stack.run_unary(func, on_all = env.on_all)
    return (stack_func, 1)

def unique_stack(env, stack):
    data = stack.clear()
    data = sorted(set(data))
    stack.push(*data)

def wait(env, stack):
    val = stack.pop()
    time.sleep(val)

def wait_millis(env, stack):
    val = stack.pop()
    time.sleep(val / 1000)

""" Assign tokens to the commands. """

COMMANDS = {

    #FORMAT: 'char' : (function, minumum operands)
    #   or:  'char' : template(args),

    # Mathematical functions
    '+': MathFunc(operator.add),
    '-': MathFunc(operator.sub),
    '*': MathFunc(operator.mul),
    '/': MathFunc(operator.floordiv),
    'e': MathFunc(operator.pow),
    'E': MathFunc(e_notation),
    '%': MathFunc(operator.mod),

    'M': MathFunc(max),
    'm': MathFunc(min),

    '=': MathFunc(operator.eq),
    '!': MathFunc(operator.ne),
    '>': MathFunc(operator.gt),
    '<': MathFunc(operator.lt),
    ')': MathFunc(operator.ge),
    '(': MathFunc(operator.le),

    # Stack manipulation
    '{': (leftshift, 1),
    '}': (rightshift, 1),
    '@': (reverse_stack, 0),
    '&': (dupe_last, 1),

    'C': (multiple_copies, 2),
    'c': (clear_stack, 1),
    'd': (copy_region, 1),
    'w': (mirror, 1),
    '.': (pop_last, 1),
    ',': (pop_first, 1),
    'u': (unique_stack, 1),
    'g': (sort_asc, 1),
    'G': (sort_desc, 1),
    'K': (op_on_all, 0),
    'k': (op_on_last, 0),

    # Cross-stack operations
    'I': (goto_in, 0),
    'O': (goto_out, 0),
    'F': (swap_stacks, 0),
    'x': (stack_equality, 0),
    'v': (send_to_out, 0),
    '^': (send_to_in, 0),
    'V': (copy_to_out, 0),

    # Nilads
    'Z': ConstNilad(0),
    'T': ConstNilad(10),
    'H': ConstNilad(100),
    'A': (lambda e,s: s.push(*range(65, 91)), 0),
    'a': (lambda e,s: s.push(*range(97, 123)), 0),
    'P': (product, 0),
    'S': (sum_stack, 0),
    'L': (stack_len, 0),
    'Y': (stack_ispalindrome, 0),

    # Unaries
    '|': UnaryFunc(abs),
    '~': UnaryFunc(operator.neg),
    'b': UnaryFunc(bool),
    'n': UnaryFunc(not_bool),
    'f': UnaryFunc(factorial),
    'h': UnaryFunc(head),
    'r': UnaryFunc(intsqrt),
    'p': UnaryFunc(primality),
    't': UnaryFunc(tail),
    'l': UnaryFunc(digit_length),
    'y': UnaryFunc(ispalindrome),

    # Other
    'U': (get_random, 2),
    'W': (wait, 1),
    'i': (interrupt, 0),
    's': (split_int, 1),
    'j': (join_ints, 2),
    'R': (push_inc_range, 1),
    'X': (push_range, 1),
    'z': (ternary, 3),

    # Output commands
    '#': (print_int, 1),
    '_': (print_stack, 0),
    "'": (print_char, 1),
    '"': (print_charcodes, 0),
    'Q': (out_uppercase, 0),
    'q': (out_lowercase, 0),
    'D': (set_delim, 1),
    'N': (no_delim, 0),


    # EXTRA COMMANDS
    # These commands are accessed by being prefixed with an 'o'.

    # Bitwise/Binary Functions
    'o>' : MathFunc(operator.rshift),
    'o<' : MathFunc(operator.lshift),
    'o&' : MathFunc(operator.and_),
    'o|' : MathFunc(operator.or_),
    'o^' : MathFunc(operator.xor),
    'ol' : UnaryFunc(int.bit_length),
    'o~' : UnaryFunc(operator.invert),
    'oB' : (tobinary, 1),

    # Misc Functions
    'op' : (prime_filter, 0),
    'og' : (is_sorted_asc, 0),
    'oG' : (is_sorted_desc, 0),
    'o=' : (all_equal, 0),
    'ou' : (is_set, 0),
    'o/' : MathFunc(math.gcd),
    'o*' : MathFunc(lcm),
    'oI' : (copy_input, 0),
    'od' : (multiply_stack, 1),
    'oS' : (shuffle_stack, 1),
    'oW' : (wait_millis, 1),

}

LOOP_TOKENS = {

    '?': IfStatement,
    ':': ForLoop,
    '$': WhileLoop,
    '[': InfLoop,

}

BACK = ';'
BREAK = 'B'

STRING_MODE = '`'
COMMENT = '\\'
COMMENT_ESC = '\n'

class IO_Util:
    def __init__(self, delim = '\n'):
        self.delim = delim

    def set_delim(self, text):
        self.delim = text

    def out(self, *values):
        print(*values, end = self.delim)
        sys.stdout.flush()
        self.last_sep = self.delim

    def err(self, text):
        # Start error on newline.
        if '\n' != self.last_sep: print()

        print(text, file = sys.stderr)
        quit()

class Env:
    def __init__(self, ins, io = None):
        if io == None: io = IO_Util()

        self.inputs = ins
        self.io = io
        self.on_all = False

        self.IN = Stack(*ins)
        self.OUT = Stack()

        # True if focus is on IN stack.
        # False if focus is on OUT stack.
        self.focus = True

    def curr_stack(self):
        if self.focus:
            return self.IN
        return self.OUT

    def swap_stacks(self):
        self.IN, self.OUT = self.OUT, self.IN

    def switch_stacks(self):
        self.focus = not self.focus

    def __repr__(self):
        return repr(self.IN) + ', ' + repr(self.OUT)

class Script:
    def __init__(self, script_text, io = None):
        if io == None:
            io = IO_Util()
        self.io = io

        self.tokens = self.to_tokens(script_text)

    @staticmethod
    def to_tokens(text):
        """ Tokenizer function. Takes a Pushy script and tokenizes it.
        Adjacent integers are grouped together, but leading zeroes are parsed seperately.
        Anything after a 'o' is grouped with it, parsed as a special command - except for string/comment mode chars. """

        return re.findall(r'o[^`]|0|[1-9]+\d*|[^\d]', text)

    def run(self, inputs = None):
        if inputs == None:
            inputs = []

        env = Env(inputs, self.io)

        i = -1
        skip = 0
        loops = []

        stringmode, currstring = False, ''
        commentmode = False

        while True:
            i += 1

            if i >= len(self.tokens):

                if len(loops) < 1:
                    break

                if stringmode:
                    break

                if commentmode:
                    commentmode = False

                skip = 0
                l = loops[0]

                if l[0].verify(env):
                    i = l[1]
                else:
                    loops.pop(0)

                continue

            char = self.tokens[i]

            if char == COMMENT:
                if not stringmode:
                    commentmode = True
                    continue

            if commentmode:
                commentmode = (char != COMMENT_ESC)
                continue

            if char == STRING_MODE:
                stringmode = not stringmode

                if stringmode == False:
                    env.curr_stack().push(*[ord(ch) for ch in currstring])
                    currstring = ''
                continue

            if stringmode:
                currstring += char
                continue

            if skip:
                if not (stringmode or commentmode):
                    if char in LOOP_TOKENS:
                        skip += 1
                    elif char == BACK:
                        skip -= 1
                continue

            if char in LOOP_TOKENS:
                newloop = (LOOP_TOKENS[char](env), i)

                if newloop[0].verify(env):
                    loops.insert(0, newloop)
                else:
                    skip += 1
                continue

            if char == BACK:
                if len(loops) < 1:
                    continue

                l = loops[0]

                if l[0].verify(env):
                    i = l[1]
                else:
                    loops.pop(0)
                continue

            if char.isdigit():
                env.curr_stack().push(int(char))
                continue

            if char in COMMANDS:
                cmd = COMMANDS[char]

                if cmd[1] <= len(env.curr_stack()):
                    cmd[0](env, env.curr_stack())

                continue

        return env

# All the necessary classes, dicts, etc, are now set up.
# Programs are run using Script(<text>).run(<inputs>).
