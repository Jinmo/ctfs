#!/bin/bash

echo Solution only.
echo It didn\'t contain processes for solution

cp ../challenge/pocket .
file pocket
echo 'Step 0. extract pocket as ZIP'
echo
unzip -o pocket
echo ===
echo 'Step 1. extract biscuit as RAR'
echo
file biscuit
unrar e -o+ biscuit
echo ===
echo 'Step 2. get password from biscuit1 (exe) for biscuit2'
echo
file biscuit1 biscuit2
echo
echo ': Run biscuit1 as EXE and get flag by setting breakpoint in free()'
echo 'It says "Please find sweets name starting from m for biscuit2."'
echo
echo '.text:00401711 mov     eax, [esp+0B4h+var_9C]'
echo '.text:00401715 mov     [esp+0B4h+Str], eax             ; Memory'
echo '.text:00401718 call    _free'
echo

echo On .text:0x401715,
echo "EAX | debug019:00AE1658 aMacaron db 'macaron',0"

echo
echo Extracting biscuit2 with password \'macaron\'...
unzip -o -Pmacaron biscuit2

echo ===
echo Step 3. Get flag from three files
file biscuit3 biscuit4 biscuit5

echo cat biscuit4
cat biscuit4
echo

echo ---
echo ... and biscuit3 has ZIP at the end of file

read -r cmd <<CMD
python -c 'print open("biscuit3", "rb").read().split("\xff\xd9")[1]' > biscuit3.zip
CMD
echo "$cmd"
eval "$cmd"
file biscuit3.zip
unzip -o biscuit3.zip
cmd='cat biscuit.txt'
echo $cmd
eval '$cmd'
echo

echo So, biscuit3: cream
echo For biscuit5, add breakpoint at 0x401694
echo
echo .text:00401694                 mov     eax, 0
echo .text:00401699                 lea     esp, [ebp-8]
echo .text:0040169C                 pop     ebx
echo
echo EDX \| Stack[00000F74]:0060FE77 aChoux db \'choux\',0
echo
echo So biscuit5: choux
echo But wtf\?\! The flag was TMCTF{choux_cream}
echo it was not TMCTF{cream_choux}, when I tried.
echo
echo Well.. ok thanks for reading\!
echo Flag: TMCTF{choux_cream}