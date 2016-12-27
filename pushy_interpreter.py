"""
Pushy Interpreter - Version 2 (rewrite)
Created 26/12/16
"""

import math
import operator
import random
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
            if type(v) in (int, float):
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

""" Define all commands to be used in the interpreter. """

def clear_stack(env, stack):
    stack.clear()

def ConstNilad(*value):
    def stack_func(env, stack):
        stack.push(*value)
    return (stack_func, 0)

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
    quit()

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
    data = stack.copy()[1:]
    stack.push(*data[::-1])

def multiple_copies(env, stack):
    copies = stack.pop()
    value = stack.pop(peek = True)
    for i in range(copies):
        stack.push(value)

def no_delim(env, stack):
    env.io.set_delim('')

def not_bool(x):
    return int(x == 0)

def op_on_all(env, stack):
    env.on_all = True

def op_on_last(env, stack):
    env.on_all = False

def out_lowercase(env, stack):
    s = [ord('a') + i % 26 for i in stack]
    env.io.out(s)

def out_uppercase(env, stack):
    s = [ord('A') + i % 26 for i in stack]
    env.io.out(s)

def pop_first(env, stack):
    stack.pop(index = 0)

def pop_last(env, stack):
    stack.pop()

def primality(num):
    #TODO: Optimize prime function!

    if num < 2:
        return False
    if num == 2:
        return True
    if num == 3:
        return True

    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0: return False

    return True

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
    stack.push(*range(1, val+1))

def push_range(env, stack):
    val = stack.pop()
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

}

# (Testing/Dev function)
def remaining_chars():
    all_chars = map(chr, range(32, 127))
    left = ''
    for c in all_chars:
        if c.isdigit():
            continue
        if c in COMMANDS.keys():
            continue
        left += c
    return left

#==== this comment is a marker (delete later pls) ====#

class IO_Util:
    def __init__(self, delim = '\n'):
        self.delim = delim

    def set_delim(self, text):
        self.delim = text

    def out(self, *values):
        print(*values, end = self.delim)
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
