#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include "script.h"


char* fgets_eof(char* buf, size_t len)
{
    char* retval = fgets(buf, len, stdin);
    if(feof(stdin))
    {
        printf("EOF reached\n");
        exit(0);
    }
    if(strlen(buf) >= 1 && buf[strlen(buf)-1]=='\n')
        buf[strlen(buf)-1] = '\x00';
    return retval;
}


int execute(char* buf)
{
    struct AST_parser* x = new_AST_parser(buf);
    struct AST_tree* tree = AST_parser_parse(x);
    if(!tree) 
    {
        del_AST_parser(x);
        return 0;
    }
    struct VAL_cell* result = AST_tree_eval(tree, NULL);
    //AST_tree_print(tree);
    VAL_cell_print(result);
    del_AST_tree(tree);
    del_AST_parser(x);
    del_VAL_cell(result);
    return 0;
}
