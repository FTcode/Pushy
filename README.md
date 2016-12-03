# Pushy
Pushy is an esoteric programming language. The name comes from its data structure, two LIFO stacks, on which one "pushes" operands for different operations. Although it was not designed for [code golf](https://en.wikipedia.org/wiki/Code_golf), its tokenized syntax and range of builtins often result in rather concise code.

To run a pushy script, download both scripts in this git and use the command-line syntax: `$ pushy <source-file> [input]`.

## Example Programs

### Hello World:

    `Hello, World!`"
    
This is rather straightforward. Any text wrapped in backticks is interpreted as a "string" - but Pushy only uses integers, so the ASCII codepoint of each character is pushed to the current stack. The `"` operator then takes all values in the stack, interprets them as characters, and prints.

### Quine:

_(a quine is a program which outputs its own source code)_

    95 34
    _"
    
This is the shortest known quine for Pushy. First, 95 and 34 are pushed to the stack. Then, `_` outputs a "representation" of the stack - its values, seperated by spaces (resulting in `95 34`, with a trailing newline). As mentioned earlier, the `"` outputs the stack as a string. 95 and 34 are the Unicode codes for `_` and `"`, so the bottom line is printed.

### Numbers 1-10:

    TR_
    
`T` is a shortcut for `10` - a numeric literal which is pushed to the stack. `R` then takes the last value (we'll call it **n**) and creates the range 1 to **n** - inclusively. `_` then outputs the current stack, containing this range, seperated by spaces:

    1 2 3 4 5 6 7 8 9 10
