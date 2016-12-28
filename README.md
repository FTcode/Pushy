# Pushy

A stack-based, esoteric programming language.

You can try Pushy via the [online interpreter](https://tio.run/nexus/pushy), provided by @DennisMitchell.

If you want to run a script locally, download `pushy.py` and `pushy_interpreter.py`. You can then use the following syntax on the command line:

 - `$ pushy f <script-file> [input]`: Open the given file and run as a Pushy script. Input is an (optional) Python 3 literal.
 - `$ pushy t <script-text> [input]`: Directly run the second argument as a Pushy script.

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

## Docs

Coming soon, one day...
