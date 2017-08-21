#ifndef __ASTPARSER__
#define __ASTPARSER__
#include "asttree.h"

struct AST_parser
{
    int loc;
    char* buf;
};

struct AST_parser* new_AST_parser(char* buf);
struct AST_tree* AST_parser_parse(struct AST_parser* self);
void del_AST_parser(struct AST_parser* self);
#endif
