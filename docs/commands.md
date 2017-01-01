# Pushy: Command List

**Notes:**

 - Pushy has 2 stacks, but at any given time, there is one stack in focus. This is called the "current stack". All operations, unless otherwise specified, act on the current stack.
 - Commands have a _minimum arity_ - how many items they require on the stack to act. If there are not enough items, the command will be ignored.
 - Pushy uses integers only, but booleans are represented as 0 (false) and 1 (true).

---

### Stack Transformation:

 - `{` - Cyclically shift the stack left, once.
 - `}` - Cyclically shift the stack right, once.
 - `@` - Reverse the stack.
 - `.` - Delete the last item on the stack.
 - `,` - Delete the first item on the stack.
 - `&` - Push a copy of the last item.
 - `c` - Clear the stack.
 - `w` - Mirror the stack (reflect it around the central item).
 - `d` - Pop an integer, `n`, then make copies of the last `n` items on stack.
 - `C` - Pop an item, and copy the item before that many times. 
 - `u` - Make the stack a set of itself - removing all duplicate items. Then sort it ascendingly.
 - `g` - Sort the stack in ascending order.
 - `G` - Sort the stack in descending order.

### Value-Pushing Commands

These are the commands which push items on to the current stack, without popping anything:

 - `` `text` `` - Any text in backticks is a string token. As Pushy only uses integers, each character in the string has its unicode code point pushed to the stack, from left to right.
 - `0123456789` - Numeric literals. Any adjacent digits in the code are grouped together and parsed as a single token, which pushes its value to the stack. Note that leading zeroes are parsed seperately, so `01` pushes `0` and then `1`.
 - `Z` - Push 0
 - `T` - Push 10
 - `H` - Push 100
 - `A` - Push the integers in the range `65-90`, the uppercase ASCII alphabet.
 - `a` - Push the integers in the range `97-122`, the lowercase ASCII alphabet.
 - `P` - Push the product of all integers on the stack. [An empty stack has a product of 1.](https://en.wikipedia.org/wiki/Empty_product)
 - `S` - Push the sum of all integers on the stack.
 - `L` - Push the length of the stack,
 - `Y` - Check if the stack is palindromic: push 0 or 1 accordingly.

### Postfix (Math) Operations

Firstly, the K flag is very important. It can be toggled like so:

 - `K` - Set the **K flag** to True
 - `k` - Set the **K flag** to False (default)

The state of the K-flag affects the behaviour of commands in the list below. If false, these operations simply pop 2 items off the stack, perform the operation*, and push the result. However, if the K-flag is True, the top item is popped and then used to perform the operation on _all stack items_. 

<sub>* In operations where order matters, the operands are used in the order they were placed on the stack, so `10 5 /` performs `10 / 5`.</sub>

- `+` - Addition
- `-` - Subtraction
- `*` - Multiplication
- `/` - Floor division (rounded towards negative infinity)
- `%` - Modulo Operation
- `e` - Exponentiaton
- `E` - E-notation: (`A, B -> A * 10 ** B`)
- `M` - `max(a, b)`
- `m` - `min(a, b)`

Similarly, the inequality operations push 0 or 1 depending on their truthiness:

 - `=` - Equality (check if items have the same value)
 - `!` - Not equal (check if items have different values)
 - `>` - "Strictly greater than"
 - `<` - "Strictly less than"
 - `)` - "Greater than or equal to"
 - `(` - "Smaller than or equal to"

If a mathematical error is encountered, the result is by default 0.

### Cross-Stack Operations

All input is automatically copied onto stack 1, and so it is usually referred to as the `IN` stack. Accordingly, stack 2 is often referred to as the `OUT` stack.

 - `I` - Go to the `IN` stack.
 - `O` - Go to the `OUT` stack.
 - `F` - Swap the stacks around (copy `I` into `O`, and `O` into `I`)
 - `x` - Push 0 (false) or 1 (true) to the current stack, depending on whether the stacks are identical.
 - `v` - Pop an item from `IN` and push it to `OUT`.
 - `^` - Pop an item from `OUT` and send it to `IN`.
 - `V` - Copy the `IN` stack into the `OUT` stack.

### Loops

Loops are an important part of the Pushy syntax. All loops are opened with a certain character, and closed with `;`. Missing semi-colons at the end of a program are automatically inserted by the interpreter.

 - `:` - For loop: pop a value, and iterate the loop that many times. If the stack is empty, this performs 0 iterations.
 - `$` - While loop: while the last item on stack is positive, keep iterating. If the stack is empty, the loop is broken out of.
 - `?` - If statement (this is not technically a loop, but has the same syntax): pop a value, and run the code if it is non-zero. Otherwise, skip the code block.
 - `[` - Infinite loop: keep looping until the program finishes, or the loop is broken out of.
 - `;` - End loop: this character signifies the end of a code block.
 - `B` - Break: break out of all loops (regardless of nested depth).

### Output Commands

 - `#` - Print the last value on the stack, as an integer.
 - `_` - Print the whole stack, with items space-seperated. This is mainly for debugging.
 - `'` - Interpret the last item's absolute value as a unicode character, and print it.
 - `"` - Interpret the whole stack as a list of unicode characters, and print the resulting string.
 - `Q` - Copy the stack's values into a new list, modulo each value by 26, and then interpret these as indexes into the uppercase ASCII alphabet, and print the resulting string.
 - `q` - Copy the stack's values into a new list, modulo each value by 26, and then interpret these as indexes into the lowercase ASCII alphabet, and print the resulting string.
 - `D` - Set the printing delimiter to the last item on stack (character code). By default, this is char 10, a linefeed.
 - `N` - Disable the printing delimiter.

### Mapping Operations

Mapping operations, as the name suggests, map integer values to new values. If the K-flag is True, the operation is done on all stack items. Otherwise, it is only done on the last. The mapping functions are listed here:

 -  `~` - Negation
 - `|` - Absolute value
 - `f` - Factorial function
 - `h` - Increment (by 1)
 - `t` - Decrement (by 1)
 - `r` - Integer square root [(Wiki)](https://en.wikipedia.org/wiki/Integer_square_root)
 - `p` - Primality check (boolean)
 - `y` - Palindrome check - pushes the boolean of whether the number is a palindrome in base 10.
 - `l` - Digit length (maps each integer to the number of digits in its base 10 representation).
 - `b` - Boolean conversion. Maps everything to `1`, unless it is `0`.
 - `n` - Negative boolean conversion (opposite of `b`).

### Miscellaneous Commands

 - `W` - Pop an integer, wait that many seconds.
 - `U` - Pop two integers, and get a random integer between them.
 - `i` - Terminate the program.
 - `s` - Spilt an integer into its base 10 digits. For example, pop `123`, and push `1, 2, 3`.
 - `j` - Concatenation. If the K-flag is True, this pops all stack items, joins them into one large integer, and pushes the result. Otherwise, this pops the last 2 items and pushes their concatenation. Only the first integer in a concatenation sequence keeps its sign.
 - `R` - Pop an integer and push range(0, n) - not including 0, but including `n`. 
 - `X` - Pop an integer and push range(0, n) - including 0, but not including `n`. 
 - `z` - The ternary operator. Pop A, then B, then C. If A is non-zero, push B. Otherwise, push C.
