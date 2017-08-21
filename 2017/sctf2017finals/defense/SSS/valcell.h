#ifndef __VALCELL__
#define __VALCELL__

#include "asttree.h"
#include "valenv.h"


enum value_type
{
    INT,
    STRING,
    SYMBOL,
    LIST,
    BOOL,
    FUNC
};


struct VAL_cell
{
    enum value_type type;
    long long intval;
    char* strval;
    struct VAL_cell* left;
    struct VAL_cell* right;
    struct VAL_env* env;
    struct AST_tree* body;
};


void VAL_cell_repr(struct VAL_cell* self);
void VAL_cell_print(struct VAL_cell* self);
struct VAL_cell* new_INT_VAL_cell(long long value);

struct VAL_cell* new_STR_VAL_cell(char* strval);

struct VAL_cell* new_SYM_VAL_cell(char* sym);

struct VAL_cell* new_LIST_VAL_cell(struct VAL_cell*, struct VAL_cell*);

struct VAL_cell* new_BOOL_VAL_cell(int value);

struct VAL_cell* new_FUNC_VAL_cell(struct VAL_cell*, struct AST_tree*, struct VAL_env*);

struct VAL_cell* VAL_cell_deepcopy(struct VAL_cell*);

void del_VAL_cell(struct VAL_cell* self);

#endif
