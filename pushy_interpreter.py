"""
Interpreter for Pushy (rewrite)
Created 26/12/16
"""

import sys
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

""" Define all commands to be used in the interpreter. """

def clear_stack(env, stack):
    stack.clear()

def dupe_last(env, stack):
    stack.push(stack.pop(peek = True))

def leftshift(env, stack):
    # Arity: > 1
    stack.push(stack.pop(index = 0))

def mirror(env, stack):
    data = stack.copy()[1:]
    stack.push(*data)

def pop_first(env, stack):
    stack.pop(index = 0)

def pop_last(env, stack):
    stack.pop()

def rightshift(env, stack):
    # Arity: > 1
    stack.insert(0, stack.pop())

def reverse_stack(env, stack):
    data = stack.clear()
    stack.push(*reversed(data))



""" Assign tokens to the commands. """

COMMANDS = {

    #FORMAT: 'char' : (function, minumum operands)

    # Stack manipulation
    '{': (leftshift, 1),
    '}': (rightshift, 1),
    '@': (reverse_stack, 0),
    '&': (dupe_last, 1),
    
    'c': (clear_stack, 0),
    'w': (mirror, 0),
    '.': (pop_last, 1),
    ',': (pop_first, 1),

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

class PushyEnv:
    def __init__(self, io, *ins):
        self.inputs = ins
        self.io = io

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
