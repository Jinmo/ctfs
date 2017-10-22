## Scriptabble

Run-only applescript reversing. This is disassembler for that.

## What is it all about?

To write disassembler I reversed vm routine, file format (fas, uas) in applescript binary.

- disassembler.py uses fasparser.py to parse format and extract literal table & code and disassemble it.
- fasparser.py parses compiled scpt file. If it's compiled without -x (run only mode), it would have error on cmdBlock parsing, for now.
- examples/solve.py is flag-generation related routine of `example/apple.scpt` ported to python, and it works fastly in PyPy.

** WARNING: ** It only implemented parts used in `examples/apple.scpt`.
