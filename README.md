# Pushy
Pushy is an esoteric programming language. The name comes from its data structure, two [LIFO stacks](https://en.wikipedia.org/wiki/Stack_(abstract_data_type)), on which one "pushes" operands for different operations. Although it was not designed for [code golf](https://en.wikipedia.org/wiki/Code_golf), its tokenized syntax and range of builtins often result in rather concise code.

You can try Pushy via the [online interpreter](https://tio.run/nexus/pushy), provided by @DennisMitchell. Or, to run a script locally, download both scripts in this git and use the command-line syntax: `$ pushy <source-file> [input]`.

## Example Programs

### Hello World:

    `Hello, World!`"
    
This is rather straightforward. Any text wrapped in backticks is interpreted as a "string" - but Pushy only uses integers, so the ASCII codepoint of each character is pushed to the current stack. The `"` operator then takes all values in the stack, interprets them as characters, and prints.

### Quine:

_(a quine is a program which outputs its own source code)_

    95 34
    _"
    
This is the shortest known quine for Pushy. First, 95 and 34 are pushed to the stack. Then, `_` outputs a "representation" of the stack - its values, seperated by spaces (resulting in `95 34`, with a trailing newline). As mentioned earlier, the `"` outputs the stack as a string. 95 and 34 are the Unicode codes for `_` and `"`, so the bottom line is printed.

### Bits -> Maxsize

This program takes input from the command line, a number of bits, and prints the maximum value for an unsigned number of that size.

    2{et#

- `2{` inserts 2 before the given value **n**, so the stack is now `[2, n]`.
- `e` exponentiates these, yielding **2<sup>n</sup>**. 
- `t` is the "tail" operator, it decrements the last item.
- `#` then prints the value.
    

