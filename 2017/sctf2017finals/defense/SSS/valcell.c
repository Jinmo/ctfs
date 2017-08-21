#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "valcell.h"


struct VAL_cell* new_VAL_cell()
{
    struct VAL_cell* self = (struct VAL_cell*)malloc(sizeof(struct VAL_cell));
    memset(self, '\x00', sizeof(struct VAL_cell));
    return self;
}

struct VAL_cell* new_INT_VAL_cell(long long value)
{
    struct VAL_cell* self = new_VAL_cell();
    self->type = INT;
    self->intval = value;
    return self;
}


struct VAL_cell* new_STR_VAL_cell(char* strval)
{
    struct VAL_cell* self= new_VAL_cell();
    self->type =STRING;
    int len = strlen(strval) + 1;
    self->strval = (char*)malloc(len);
    memcpy(self->strval, strval, len);
    self->strval[len-1] = '\x00';
    return self;
}
struct VAL_cell* new_SYM_VAL_cell(char* sym)
{
    struct VAL_cell* self= new_VAL_cell();
    self->type = SYMBOL;
    int len = strlen(sym) + 1;
    self->strval = (char*)malloc(len);
    memcpy(self->strval, sym, len);
    self->strval[len-1] = '\x00';
    return self;
}

struct VAL_cell* new_BOOL_VAL_cell(int value)
{
    struct VAL_cell* self= new_VAL_cell();
    self->type = BOOL;
    self->intval = value;
    return self;

}
struct VAL_cell* new_LIST_VAL_cell(struct VAL_cell* leftn, struct VAL_cell* rightn)
{
    struct VAL_cell* self = new_VAL_cell();
    self->type = LIST;
    self->left = VAL_cell_deepcopy(leftn);
    self->right = VAL_cell_deepcopy(rightn);
    return self;
}

struct VAL_cell* new_FUNC_VAL_cell(struct VAL_cell* id, struct AST_tree* body, struct VAL_env* environ)
{
    struct VAL_cell* self = new_VAL_cell();
    self->type = FUNC;
    self->left = VAL_cell_deepcopy(id);
    self->env = VAL_env_deepcopy(environ);
    self->body = AST_tree_deepcopy(body);
    return self;
}

struct VAL_cell* VAL_cell_deepcopy(struct VAL_cell* self)
{
    struct VAL_cell* retval = new_VAL_cell();
    switch(self->type)
    {
        case INT:
            retval->type = INT;
            retval->intval = self->intval;
            break;
        case STRING:
            retval->type = STRING;
            retval->strval = (char*)malloc(strlen(self->strval) + 1);
            strcpy(retval->strval, self->strval);
            break;
        case SYMBOL:
            retval->type = SYMBOL;
            retval->strval = (char*)malloc(strlen(self->strval) + 1);
            strcpy(retval->strval, self->strval);
            break;
        case BOOL:
            retval->type = BOOL;
            retval->intval = self->intval;
            break;
        case LIST:
            retval->type = LIST;
            retval->left = VAL_cell_deepcopy(self->left);
            retval->right =VAL_cell_deepcopy(self->right);
            break;
        case FUNC:
            retval->type = FUNC;
            retval->left = VAL_cell_deepcopy(self->left);
            retval->env = VAL_env_deepcopy(self->env);
            retval->body = AST_tree_deepcopy(self->body);
    }
    return retval;
}

void del_VAL_cell(struct VAL_cell* self)
{
    if(!self) return;
    switch(self->type)
    {
        case INT:
            break;
        case STRING:
            free(self->strval);
            self->strval = NULL;
            break;
        case SYMBOL:
            free(self->strval);
            self->strval = NULL;
            break;
        case BOOL:
            break;
        case LIST:
            del_VAL_cell(self->left);
            del_VAL_cell(self->right);
            self->left = NULL;
            self->right = NULL;
            break;
        case FUNC:
            del_VAL_cell(self->left);
            del_VAL_env(self->env);
            del_AST_tree(self->body);
            self->left = NULL;
            self->env = NULL;
            self->body = NULL;
            break;
    }
    free(self);

}

void VAL_cell_recursive_print(struct VAL_cell* self)
{
    switch(self->type)
    {
        case INT:
            printf("(INT %lld)", self->intval);
            break;
        case STRING:
            printf("(STRING \"%s\")", self->strval);
            break;
        case SYMBOL:
            printf("(SYMBOL %s)", self->strval);
            break;
        case BOOL:
            if(self->intval)
            {
                printf("(BOOL true)");
            }
            else
            {
                printf("(BOOL false)");
            }
            break;
        case LIST:
            printf("(LIST ");
            VAL_cell_recursive_print(self->left);
            printf(" ");
            VAL_cell_recursive_print(self->right);
            printf(")");
            break;
        case FUNC:
            printf("(FUN ");
            AST_tree_print(self->body);
            printf(")");
            break;
    }
    return;

}
void VAL_cell_repr(struct VAL_cell* self)
{
    VAL_cell_recursive_print(self);
}
void VAL_cell_print(struct VAL_cell* self)
{
    if(!self) return;
    VAL_cell_recursive_print(self);
    printf("\n");
}
