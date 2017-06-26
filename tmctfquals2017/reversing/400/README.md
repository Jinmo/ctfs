## Reversing 400

My solution was, about hooking at all.

The binary was packed by VMProtect.
Fortunately it was solvable via dynamic analysis only.

I hooked and hooked until the program gets crashed/infinite loop.
\xeb\xfe + Cheat Engine was enough for determining what WINAPIs are used.

### Hook process

1. Since the binary moved my cursor to a button with hex character, I hooked SetCursorPos.
1. It moved some buttons, so SetWindowPos.
1. It also sleep-ed. I checked Process Hacker's stacktrace for the process to determine what API is used. Beep.
1. It also checked if it was too fast. GetTickCount, but it was not used.
1. Set-up some IPCs to dump cursor + window positions (CreatePipe). I used DuplicateHandle to communicate with the process.

## Solution code

- main.py for dumping HEXes to file
- hooklib.py is used in main.py to hook some WINAPIs.
- solution.py for decoded routine in dumped exe. Simple encryption routine to check a required password.