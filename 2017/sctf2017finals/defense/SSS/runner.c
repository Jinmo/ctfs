#include <stdio.h>
#include <stdlib.h>
#include "script.h"



void init_script()
{
    setvbuf(stdin,0,2,0);
    setvbuf(stdout,0,2,0);
    alarm(120);
}
void print_message()
{
    printf("  minimal script service\n");
    printf("  this is not well-made script, so its function is limited\n");
    printf("  declaration : \n");
    printf("\n");
    printf("    INTCONST   : 64bit signed integer\n");
    printf("    STRINGCONST: any printable characters\n");
    printf("    SYMCONST   : alphanumeric characters(max 32 characters)\n");
    printf("    INT : (add INT INT)\n");
    printf("          (sub INT INT)\n");
    printf("          (mul INT INT)\n");
    printf("          (and INT INT)\n");
    printf("          (or INT INT)\n");
    printf("          (int INTCONST)\n");
    printf("    STR : (concat STR STR)\n");
    printf("          (subst STR INT INT)\n");
    printf("          (string \"STRINGCONST\")\n");
    printf("    SYM : (sym SYMCONST)\n");
    printf("    LIST: (con ANY ANY)\n");
    printf("    FUNC: (fun SYM ANY)\n");
    printf("    BOOL: (lt INT INT)\n");
    printf("          (gt INT INT)\n");
    printf("          (eq INT INT)\n");
    printf("          (eq STR STR)\n");
    printf("          (eq BOOL BOOL)\n");
    printf("          (or BOOL BOOL)\n");
    printf("          (and BOOL BOOL)\n");
    printf("          (not BOOL)\n");
    printf("     ANY: (car LIST)\n");
    printf("          (cdr LIST)\n");
    printf("          (ite BOOL ANY ANY)\n");
    printf("          (let SYM ANY ANY)\n");
    printf("          (FUNC ANY)\n");
    printf("  example : \n");
    printf("    (add (int 1) (int 2))\n");
    printf("     - it computes 1 + 2.\n");
    printf("    (concat (string \"hello \") (string \"world!\"))\n");
    printf("     - it concatenate two strings.\n");
    printf("    (let (sym odd) (fun (sym x) (sub (mul (sym x) (int 2)) (int 1)))  ((sym odd) (int 6)))\n");
    printf("     - it computes 6th odd number.\n");
    printf("    (let (sym fib) (fun (sym x) (cdr (let (sym fibr) (fun (sym c) (ite (eq (cdr (sym c)) (int 0)) (con (car (sym c)) (int 0)) (ite (eq (cdr (sym c)) (int 1)) (con (car (sym c)) (int 1)) (con (car (sym c)) (add (cdr ((car (sym c)) (con (car (sym c)) (sub (cdr (sym c)) (int 1))))) (cdr ((car (sym c)) (con (car (sym c)) (sub (cdr (sym c)) (int 2)))))))))) ((sym fibr) (con (sym fibr) (sym x)))))) ((sym fib) (int 13)))\n");
    printf("     - it computes 13th fibonacci number.\n");
}
int main()
{
    init_script();
    print_message();
    char linebuf[0x10000];
    int errorno;
    while(1)
    {
        printf(">> ");
        fgets_eof(linebuf, 0x1000);
        if(errorno = execute(linebuf))
        {
            printf("error occured, eno=%d\n", errorno);
        }
    }
}
