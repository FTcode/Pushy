# == Pushy Interpreter == #
# Created 15/11/2016

import re, string, sys, math, time, functools, random

class Stack(list):
    def __init__(self, *v):
        self.push(*v)
        self.OP_ALL = False

    def push(self, *v):
        for x in v: super().append(int(x))


    def pop(self, i = -1, peek = False):
        if len(self) < 1 : raise Exception("Cannot take args/values from empty stack.")
        return self[i] if peek else super().pop(i)

    def clear(self):
        del self[:]

    def shiftLeft(self): self.push(self.pop(0))
    def shiftRight(self): self.insert(0, self.pop())

    def runMathFunc(self, func):
        val = self.pop()
        if self.OP_ALL:
            for x in range(len(self)):
                self[x] = func(self[x], val)
            return
        self.push(func(self.pop(), val))

    def runXfunc(self, func):
        if self.OP_ALL:
            for x in range(len(self)):
                self[x] = int(func(self[x]))
            return
        self.push(int(func(self.pop())))
        

class Env:
    def __init__(self, *v):
        self.IN = Stack(*v)
        self.OUT = Stack()
        self.FOCUS = 0
        self.io = IO_Util()

    def currStack(self):
        return [self.IN, self.OUT][self.FOCUS]

    def setFocus(self, f):
        self.FOCUS = f

    def opAll(self, b):
        self.IN.OP_ALL = b
        self.OUT.OP_ALL = b

    def swapStacks(self):
        self.IN, self.OUT = self.OUT, self.IN

#======= Loop Classes =======#

class Loop:
    def __init__(self, index, env) -> None: pass
    def verify(self, env) -> bool : pass

class WhileLoop(Loop):
    def __init__(self, index, env):
        self.index = index
    
    def verify(self, env):
        s = env.currStack()
        if len(s) < 1 : return False
        return bool(s[-1])

class ForLoop(Loop):
    def __init__(self, index, env):
        self.index = index
        s = env.currStack()
        if len(s) < 1 : self.itersleft = 0
        else: self.itersleft = s.pop()

    def verify(self, env):
        v = self.itersleft > 0
        if v : self.itersleft -= 1
        return v

class IfStatement(Loop):
    def __init__(self, index, env):
        self.index = index
        s = env.currStack()
        if len(s) <= 0 : self.valid = False
        else: self.valid = bool(s.pop())

    def verify(self, env):
        v = self.valid
        self.valid = False
        return v

#======= Commands =======#

# Template for simple mathematical operation
def MathFunc(op):
    l = eval('lambda a,b: int(a'+op+'b)')
    def f(e, s): s.runMathFunc(l)
    return f

# Template for command which maps an integer to a new value
def XFunc(func):
    return (lambda e,s: s.runXfunc(func))

def factorial(x):
    if x <= 2 : return x
    return math.factorial(x)

# Template for command which pushes a constant value
def PushValCmd(val):
    return (lambda e,s: s.push(val))

# Integer sqrt of n: the largest whole number, x, where x < n**2
def isqrt(n):
    x = n
    while True:
        y = (n//x+x)//2
        if x <= y: return x
        x = y

def isPrime(num):
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0: return False
    return True

def notbool(x): return not x
def negate(x): return -x

def copyRegion(e, s):
    val = s.pop()
    s.push(*[x for x in s[-val:]])

def maximum(e, s):
    val = s.pop()
    s.runXfunc(lambda x:max(val, x))

def minimum(e, s):
    val = s.pop()
    s.runXfunc(lambda x:min(val, x))

def isPalindrome(x):
    s = str(x)
    return s == s[::-1]

def copyLast(e, s):
    t = s.pop()
    val = s.pop()
    for i in range(t): s.push(val)

def concatInts(*n):
    return int(str(n[0])+''.join([str(abs(x)) for x in n[1:]]))

def joinInts(e, s):
    if s.OP_ALL:
        data = list(s)
        del s[:]
        s.push(concatInts(*data))
    else:
        n1,n2 = s.pop(), s.pop()
        s.push(concatInts(n2, n1))

def product(*li):
    if len(li) == 0: return 0
    return functools.reduce(lambda x, y: x * y, li, 1)

def getRandom(e, s):
    n1,n2=s.pop(),s.pop()
    s.push(random.randint(min(n1,n2), max(n1,n2)))

def sortStack(e, s):
    vals = s[:]
    del s[:]
    s.push(*sorted(vals))

def sortStackDescending(e, s):
    vals = s[:]
    del s[:]
    s.push(*sorted(vals, reverse = True))

def copyInToOut(e, s):
    e.OUT.clear()
    vals = e.IN[:]
    e.OUT.push(*vals)

def interrupt(e, s):
    quit()

def uniqueStack(e, s):
    vals = []
    for x in s:
        if x not in vals: vals.append(x)
    del s[:]
    s.push(*vals)

STACK_CMDS = {

    '+' : MathFunc('+'),
    '-' : MathFunc('-'),
    '*' : MathFunc('*'),
    '/' : MathFunc('//'),
    '%' : MathFunc('%'),
    'e' : MathFunc('**'),
    'E' : MathFunc('*10**'),

    '<' : MathFunc('<'),
    '(' : MathFunc('<='),
    '=' : MathFunc('=='),
    '!' : MathFunc('!='),
    ')' : MathFunc('>='),
    '>' : MathFunc('>'),

    '}' : (lambda e,s: s.shiftRight()),
    '{' : (lambda e,s: s.shiftLeft()),
    '@' : (lambda e,s: s.reverse()),
    '&' : (lambda e,s: s.push(s.pop(peek = True))),
    'd' : copyRegion,
    'c' : (lambda e,s: s.clear()),
    'C' : copyLast,
    '.' : (lambda e,s: s.pop()),
    ',' : (lambda e,s: s.pop(0)),
    'w' : (lambda e,s: s.push(*s[::-1][1:])),

    'x' : (lambda e,s: s.push(e.IN == e.OUT)),

    '|' : XFunc(abs),
    '~' : XFunc(negate),
    
    'T' : PushValCmd(10),
    'H' : PushValCmd(100),
    'Z' : PushValCmd(0),
    
    'b' : XFunc(bool),
    'f' : XFunc(factorial),
    'h' : XFunc(lambda x:x+1),
    'n' : XFunc(notbool),
    'r' : XFunc(isqrt),
    't' : XFunc(lambda x:x-1),
    'p' : XFunc(isPrime),
    'l' : XFunc(lambda x:len(str(abs(x)))),

    's' : (lambda e,s: s.push(*str(abs(s.pop())))),
    'j' : joinInts,
    'g' : sortStack,
    'G' : sortStackDescending,
    'u' : uniqueStack,
    
    'y' : XFunc(isPalindrome),
    'Y' : (lambda e,s: s.push(s[::-1] == s)),
    'L' : (lambda e,s: s.push(len(s))),

    'M' : maximum,
    'm' : minimum,

    'R' : (lambda e,s: s.push(*range(1,abs(s.pop())+1))), 
    'X' : (lambda e,s: s.push(*range(abs(s.pop())))),
    'P' : (lambda e,s: s.push(product(*s))),
    'S' : (lambda e,s: s.push(sum(s))),
    'U' : getRandom,

    'K' : (lambda e,s: e.opAll(True)),
    'k' : (lambda e,s: e.opAll(False)),

    'A' : (lambda e,s: s.push(*[ord(x) for x in string.ascii_uppercase])),
    'a' : (lambda e,s: s.push(*[ord(x) for x in string.ascii_lowercase])),

    'I' : (lambda e,s: e.setFocus(0)),
    'O' : (lambda e,s: e.setFocus(1)),
    'F' : (lambda e,s: e.swapStacks()),

    '^' : (lambda e,s: e.IN.push(e.OUT.pop())),
    'v' : (lambda e,s: e.OUT.push(e.IN.pop())),
    'V' : copyInToOut,

    '#' : (lambda e,s: e.io.out(s[-1])),
    '_' : (lambda e,s: e.io.out(*s)),
    '"' : (lambda e,s: e.io.out(''.join(chr(abs(x)) for x in s))),
    "'" : (lambda e,s: e.io.out(chr(abs(s[-1])))),
    'Q' : (lambda e,s: e.io.out(''.join((chr(ord('A') + x%26)) for x in s))),
    'q' : (lambda e,s: e.io.out(''.join((chr(ord('a') + x%26)) for x in s))),
    'D' : (lambda e,s: e.io.setSep(chr(abs(s.pop())))),
    'N' : (lambda e,s: e.io.setSep('')),
    
    'i' : interrupt,
    'W' : (lambda e,s: time.sleep(s.pop())),
    
}

BACK = ';'
STRING_MODE = '`'
BREAK = '\\'


LOOP_CHARS = {

    '?' : IfStatement,
    '$' : WhileLoop,
    ':' : ForLoop,
    
}

#Test func
#Currently uses ASCII, will use ISO-8859-1 if more commands are needed.
def remainingLetters():
    for i in [chr(x) for x in range(33,127)]:
        if i not in (''.join(LOOP_CHARS.keys()) + ''.join(STACK_CMDS.keys()) + BACK + STRING_MODE + BREAK) and not i.isdigit(): print(end=i)

class IO_Util:
    def __init__(self):
        self.sep = '\n'
        self.lastsep = '\n'

    def out(self, *msg, end = None):
        if end == None: end = self.sep
        self.lastsep = end
        print(*msg, file = sys.stdout, end = end)
        sys.stdout.flush()

    def err(self, *msg):
        if self.lastsep != '\n': print(end='\n')
        print(*msg, file = sys.stderr)

    def setSep(self, new): self.sep = new

class Script:
    def __init__(self, scriptText):
        self.script = self.toTokens(scriptText)
        
    def toTokens(self, script) -> list:
        # Group adjacent digits together.
        t = re.findall('[^\d]|\d+',script)
        return t

    def run(self, *v):
        i = -1
        env = Env(*v)
        loops = []
        skip = 0
        stringMode = False
        currString = ''

        try:
            while True:
                i += 1

                if i >= len(self.script):
                    if len(loops) == 0: break
                    if stringMode: break
                    l = loops[-1]
                    if l.verify(env):
                        i = l.index
                    else:
                        loops.pop()
                    continue

                char = self.script[i]


                if skip:
                    if char in LOOP_CHARS:
                        skip += 1
                    elif char == BACK:
                        skip -= 1
                    continue

                if char == STRING_MODE:
                    stringMode = not stringMode
                    if not stringMode:
                        env.currStack().push(*[ord(x) for x in currString])
                    currString = ''
                    continue

                if stringMode:
                    currString += char
                    continue

                if char in string.whitespace:
                    continue

                if char in LOOP_CHARS:
                    newloop = LOOP_CHARS[char](i, env)
                    if newloop.verify(env):
                        loops.append(newloop)
                    else:
                        skip = 1
                    continue

                if char == BACK:
                    if len(loops) <= 0 : continue
                    l = loops[-1]
                    if l.verify(env):
                        i = l.index
                    else:
                        loops.pop()
                    continue

                if char == BREAK:
                    skip = len(loops)
                    del loops[:]

                if char.isdigit():
                    env.currStack().push(int(char))
                    continue
                
                if char in STACK_CMDS:
                    try:
                        STACK_CMDS[char](env, env.currStack())
                    except Exception as e:
                        env.io.err("Python error (at token "+repr(i+1)+"):",e)
                        break
                    continue
        except KeyboardInterrupt:
            env.io.err("Program terminated (keyboard interruption).")
