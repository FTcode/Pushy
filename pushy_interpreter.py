"""
Pushy Interpreter - Version 2 (rewrite)
Created 26/12/16
"""

import sys
import math
import random
import operator

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

def leftshift(env, stack):
    # Arity: > 1
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
    stack.push(*data)

def multiple_copies(env, stack):
    copies = stack.pop()
    value = stack.pop(peek = True)
    for i in range(copies):
        stack.push(value)

def not_bool(x):
    return int(x == 0)

def op_on_all(env, stack):
    env.on_all = True

def op_on_last(env, stack):
    env.on_all = False

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

def rightshift(env, stack):
    # Arity: > 1
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

def stack_equality(env, stack):
    stack.push(int(env.IN == env.OUT))

def stack_len(env, stack):
    stack.push(len(stack))

def swap_stacks(env, stack):
    env.swap_stacks()

def tail(x):
    return x - 1

def UnaryFunc(func):
    def stack_func(env, stack):
        stack.run_unary(func, on_all = env.on_all)
    return (stack_func, 1)

def unique_stack(env, stack):
    data = stack.clear()
    data = sorted(set(data))
    stack.push(*data)

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
    'c': (clear_stack, 0),
    'd': (copy_region, 1),
    'w': (mirror, 0),
    '.': (pop_last, 1),
    ',': (pop_first, 1),

    'u': (unique_stack, 0),

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
    'L': (stack_len, 0),

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

    # Other
    'U': (get_random, 2),
    'i': (interrupt, 0),

}



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
