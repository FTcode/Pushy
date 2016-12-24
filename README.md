# Pushy
Pushy is an esoteric programming language. The name comes from its data structure, two [LIFO stacks](https://en.wikipedia.org/wiki/Stack_(abstract_data_type)), on which one "pushes" operands for different operations. Although it was not designed for [code golf](https://en.wikipedia.org/wiki/Code_golf), its tokenized syntax and range of builtins often result in rather concise code.

You can try Pushy via the [online interpreter](https://tio.run/nexus/pushy), provided by @DennisMitchell. Or, to run a script locally, download both scripts in this git and use the command-line syntax: `$ pushy <source-file> [input]`.

## Example Programs

### Hello World:

    `Hello, World!`"
    
This is rather straightforward. Any text wrapped in backticks is interpreted as a "string" - but Pushy only uses integers, so the ASCII codepoint of each character is pushed to the current stack. The `"` operator then takes all values in the stack, interprets them as characters, and prints.

[**Try it online!**](https://tio.run/nexus/pushy#@5/gkZqTk6@jEJ5flJOimKD0/z8A)

### Fibonacci Generator

This program takes input from the command line, and prints that many numbers of the fibonacci sequence.

    Z1@:2d+;_

[**Try it online!**](https://tio.run/nexus/pushy#LU@7bsMwDNz1FTc2qFHYGd2lS4cuadExTVEoMmMLlUlDjxT5eleKxYXE8Xh3XE/4SGG6YfEyej0jCkZi8joS4kS4WB8iDrmfhbUxFpzmM/nwpBTudcLbvDhrbOxheUkRNkAYIWrzq7rjxiku6KB5QKte6uEnXbMSbdQGN0tusDziq23QNeBv1VfmAdHOFDBIj4c4ZQcjHFKBeKewHx4LC5tNyZ13kMt9dDp/sMdVu0RBPVfF15zEiSzqpwLvKZbwf5O4mkhhXdeu/Qc) (commented)

### Quine:

_(a quine is a program which outputs its own source code)_

    95 34
    _"
    
[**Try it online!**](https://tio.run/nexus/pushy#@29pqmBswhWvxPX/PwA)

