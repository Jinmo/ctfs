#ifndef __ASTTREE__
#define __ASTTREE__

#include "valenv.h"
#include "valcell.h"

struct VAL_env;

enum syntax_type
{
    NIL,
    APP,
    ADD,
    SUB,
    MUL,
    CON,
    CAR,
    CDR,
    LT,
    GT,
    EQ,
    OR,
    AND,
    NOT,
    ITE,
    FUN,
    CONCAT,
    SUBST,
    LET,
    VAL
};



struct AST_tree
{
    enum syntax_type type;
    struct AST_tree* leftn;
    struct AST_tree* rightn;
    struct AST_tree* elsen;
    struct VAL_cell* value;
};


struct AST_tree* new_AST_tree();

void del_AST_tree(struct AST_tree* self);

void AST_tree_print(struct AST_tree* self);

struct VAL_cell* AST_tree_eval(struct AST_tree* self,
        struct VAL_env * environ);

struct AST_tree* AST_tree_deepcopy(struct AST_tree* self);


#endif
