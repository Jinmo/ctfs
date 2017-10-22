# light
Two files are given. One is .exe, and one is “data”.
The EXE program itself is the Lights-Out game. When the rows and cols are both 128, the flag inside the binary is xored when a tile(light) is clicked.

```c
flag[16 * (y & 1) + (x >> 3)] ^= 1 << (7 - x & 7)
```

Then the flag is showed when all lights are on. The problem states that if I load the data and turn all of the lights on, it’ll show the flag. To get the flag, I need to solve lights-out puzzle in “data” file. It’s 128 cols * 128 rows.

I solved the puzzle via the script in https://soupofentropy.wordpress.com/2016/09/05/how-to-solve-any-lights-out-games-or-my-writeup-for-lights-out-tokyo-westernsmma-ctf-2nd-2016/ .
 
After solving the puzzle, I saved the output to lights.txt and wrote the script `lightsout_solver.py` to obtain the flag.
