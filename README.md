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

    Z1@2-:2d+;_

[**Try it online!**](https://tio.run/nexus/pushy#LY8xT8QwDIX3/Io3guihtmNZWBhYDsQIh1AuzbURqV0lzqH79SVp68WW/ez3eTnhPcXxhjnwEPQEYQyWbNBiIaPFxYUoOOZ8ZtLGOFCazjbER6Wwxgmv0@ydcdLB0ZwELoIJUbT5Vc3npikuaKCpR62e98UPe82X7CatcHPW944GfNUVmgr0rdpDtyqPhxbiJhvRc4c7GbOHYYqptOheoe0fig6bUSHPM/BlLb3OP7S4ap9sVE@7@0tm8cyz@tkbb0kK/t/IfmdSWJalqf8B) (commented)

### Quine:

_(a quine is a program which outputs its own source code)_

    95 34
    _"
    
[**Try it online!**](https://tio.run/nexus/pushy#@29pqmBswhWvxPX/PwA)

