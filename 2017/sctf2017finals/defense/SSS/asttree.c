#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "asttree.h"

struct AST_tree* new_AST_tree()
{
    struct AST_tree* self = (struct AST_tree*)malloc(sizeof(struct AST_tree));
    self->type = NIL;
    self->leftn = NULL;
    self->rightn = NULL;
    self->elsen = NULL;
    self->value = NULL;
    return self;
}

void del_AST_tree(struct AST_tree* self)
{
    if(!self) return;
    if(self->leftn)
    {
        del_AST_tree(self->leftn);
    }
    if(self->rightn)
    {
        del_AST_tree(self->rightn);
    }
    if(self->elsen)
    {
        del_AST_tree(self->elsen);
    }
    if(self->value)
    {
        del_VAL_cell(self->value);
    }
    free(self);
}

struct AST_tree* AST_tree_deepcopy(struct AST_tree* self)
{
    struct AST_tree* retval = new_AST_tree();
    retval->type = self->type;
    switch(self->type)
    {
        case ITE:
        case SUBST:
        case LET:
            retval->elsen = AST_tree_deepcopy(self->elsen);
        case APP:
        case ADD:
        case SUB:
        case MUL:
        case CON:
        case LT:
        case GT:
        case EQ:
        case OR:
        case AND:
        case FUN:
        case CONCAT:
            retval->rightn = AST_tree_deepcopy(self->rightn);
        case CAR:
        case CDR:
        case NOT:
            retval->leftn = AST_tree_deepcopy(self->leftn);
        break;
        case VAL:
            retval->value = VAL_cell_deepcopy(self->value);
    }
    return retval;
}
void AST_tree_recursive_print(struct AST_tree* self)
{
    switch(self->type)
    {
        case APP:
            printf("(APP ");
            AST_tree_recursive_print(self->leftn);
            AST_tree_recursive_print(self->rightn);
            break;
        case ADD:
            printf("(ADD ");
            AST_tree_recursive_print(self->leftn);
            AST_tree_recursive_print(self->rightn);
           break;
        case SUB:
            printf("(SUB ");
            AST_tree_recursive_print(self->leftn);
            AST_tree_recursive_print(self->rightn);
           break;
        case MUL:
            printf("(MUL ");
            AST_tree_recursive_print(self->leftn);
            AST_tree_recursive_print(self->rightn);
           break;
        case CON:
            printf("(CON ");
            AST_tree_recursive_print(self->leftn);
            AST_tree_recursive_print(self->rightn);
           break;
        case CAR:
            printf("(CAR ");
            AST_tree_recursive_print(self->leftn);
           break;
        case CDR:
            printf("(CDR ");
            AST_tree_recursive_print(self->leftn);
            break;
        case LT:
            printf("(LT ");
            AST_tree_recursive_print(self->leftn);
            AST_tree_recursive_print(self->rightn);
           break;
        case GT:
            printf("(GT ");
            AST_tree_recursive_print(self->leftn);
            AST_tree_recursive_print(self->rightn);
           break;
        case EQ:
            printf("(EQ ");
            AST_tree_recursive_print(self->leftn);
            AST_tree_recursive_print(self->rightn);
           break;
        case OR:
            printf("(OR ");
            AST_tree_recursive_print(self->leftn);
            AST_tree_recursive_print(self->rightn);
           break;
        case AND:
            printf("(AND ");
            AST_tree_recursive_print(self->leftn);
            AST_tree_recursive_print(self->rightn);
           break;
        case NOT:
            printf("(NOT ");
            AST_tree_recursive_print(self->leftn);
           break;
        case ITE:
            printf("(ITE ");
            AST_tree_recursive_print(self->leftn);
            AST_tree_recursive_print(self->rightn);
            AST_tree_recursive_print(self->elsen);
            break;
        case FUN:
            printf("(FUN ");
            AST_tree_recursive_print(self->leftn);
            AST_tree_recursive_print(self->rightn);
            break;
        case CONCAT:
            printf("(CONCAT ");
            AST_tree_recursive_print(self->leftn);
            AST_tree_recursive_print(self->rightn);
            break;
        case SUBST:
            printf("(SUBST ");
            AST_tree_recursive_print(self->leftn);
            AST_tree_recursive_print(self->rightn);
            AST_tree_recursive_print(self->elsen);
            break;
        case LET:
            printf("(LET ");
            AST_tree_recursive_print(self->leftn);
            AST_tree_recursive_print(self->rightn);
            AST_tree_recursive_print(self->elsen);
            break;
        case VAL:
            VAL_cell_repr(self->value);
            return;
    }
    printf(")");
    return;
}

void AST_tree_error(struct AST_tree* self, char* msg)
{
    printf("runtime error : \"%s\"\n", msg);
    return;
}
void AST_tree_print(struct AST_tree* self)
{
    AST_tree_recursive_print(self);
    return;
}


struct VAL_cell* AST_tree_val(struct AST_tree* self, struct VAL_cell* x, struct VAL_env* environ)
{
    if(x->type != SYMBOL)
        return VAL_cell_deepcopy(x);
    else
    {
        struct VAL_env* ptr = environ;
        for(; ptr; ptr = ptr->next)
        {
            if(!strcmp(x->strval, ptr->val_name))
            {
                return VAL_cell_deepcopy(ptr->elem);
            }
        }
        AST_tree_error(self, "unbounded symbol");
        return NULL;
    }
}

struct VAL_cell* AST_tree_sym(struct AST_tree* self, struct VAL_cell *x)
{
    if(x->type != SYMBOL)
    {
        AST_tree_error(self, "invalid type (SYMBOL)");
        return NULL;
    }
    return VAL_cell_deepcopy(x);

}

struct VAL_cell* AST_tree_add(struct AST_tree* self, struct VAL_cell* x, struct VAL_cell* y)
{
    if(!(x->type == INT && y->type == INT))
    {
        AST_tree_error(self, "invalid type (INT) ");
        return NULL;
    }
    unsigned long long returnint = x->intval + y->intval;
    return new_INT_VAL_cell(returnint);

}

struct VAL_cell* AST_tree_sub(struct AST_tree* self, struct VAL_cell* x, struct VAL_cell* y)
{
    if(!(x->type == INT && y->type == INT))
    {
        AST_tree_error(self, "invalid type (INT) ");
        return NULL;
    }
    unsigned long long returnint = x->intval - y->intval;
    return new_INT_VAL_cell(returnint);

}

struct VAL_cell* AST_tree_mul(struct AST_tree* self, struct VAL_cell* x, struct VAL_cell* y)
{
    if(!(x->type == INT && y->type == INT))
    {
        AST_tree_error(self, "invalid type (INT) ");
        return NULL;
    }
    unsigned long long returnint = x->intval * y->intval;
    return new_INT_VAL_cell(returnint);
}

struct VAL_cell* AST_tree_con(struct AST_tree* self, struct VAL_cell* x, struct VAL_cell* y)
{
    return new_LIST_VAL_cell(x, y);
}

struct VAL_cell* AST_tree_car(struct AST_tree* self, struct VAL_cell* x)
{
    if(!(x->type == LIST))
    {
        AST_tree_error(self, "invalid type (LIST) ");
        return NULL;
    }
    return VAL_cell_deepcopy(x->left);
}

struct VAL_cell* AST_tree_cdr(struct AST_tree* self, struct VAL_cell* x)
{
    if(!(x->type == LIST))
    {
        AST_tree_error(self, "invalid type (LIST) ");
        return NULL;
    }
    return VAL_cell_deepcopy(x->right);
}

struct VAL_cell* AST_tree_lt(struct AST_tree* self, struct VAL_cell* x, struct VAL_cell* y)
{
    if(!(x->type == INT && y->type == INT))
    {
        AST_tree_error(self, "invalid type (INT) ");
        return NULL;
    }
    return new_BOOL_VAL_cell(x->intval < y->intval);
}

struct VAL_cell* AST_tree_gt(struct AST_tree* self, struct VAL_cell* x, struct VAL_cell* y)
{
    if(!(x->type == INT && y->type == INT))
    {
        AST_tree_error(self, "invalid type (INT) ");
        return NULL;
    }
    return new_BOOL_VAL_cell(x->intval > y->intval);
}

int AST_tree_recursive_eq(struct AST_tree* self, struct VAL_cell* x, struct VAL_cell* y)
{
    if(x->type != y->type)
        return 0;
    switch(x->type)
    {
        case INT:
            return x->intval == y->intval;
        case STRING:
            return !strcmp(x->strval, y->strval);
        case LIST:
            return AST_tree_recursive_eq(self, x->left, y->left) && AST_tree_recursive_eq(self, x->right, y->right);
        case FUNC:
            return 0;
        case SYMBOL:
            return 0;
    }
}
struct VAL_cell* AST_tree_eq(struct AST_tree* self, struct VAL_cell* x, struct VAL_cell* y)
{
    return new_BOOL_VAL_cell(AST_tree_recursive_eq(self,x,y));
}

struct VAL_cell* AST_tree_or(struct AST_tree* self, struct VAL_cell* x, struct VAL_cell* y)
{
    if(!((x->type == INT && y->type == INT) || (x->type == BOOL && y->type == BOOL)))
    {
        AST_tree_error(self, "invalid type (INT or BOOL) ");
        return NULL;
    }
    if(x->type == INT)
    {
        return new_INT_VAL_cell(x->intval | y->intval);
    }
    else
    {
        return new_BOOL_VAL_cell(x->intval | y->intval);
    }
}

struct VAL_cell* AST_tree_and(struct AST_tree* self, struct VAL_cell* x, struct VAL_cell* y)
{
    if(!((x->type == INT && y->type == INT) || (x->type == BOOL && y->type == BOOL)))
    {
        AST_tree_error(self, "invalid type (INT or BOOL) ");
        return NULL;
    }
    if(x->type == INT)
    {
        return new_INT_VAL_cell(x->intval & y->intval);
    }
    else
    {
        return new_BOOL_VAL_cell(x->intval & y->intval);
    }
}

struct VAL_cell* AST_tree_not(struct AST_tree* self, struct VAL_cell* x)
{
    if(!(x->type == BOOL))
    {
        AST_tree_error(self, "invalid type (BOOL) ");
        return NULL;
    }
    return new_BOOL_VAL_cell(!(x->intval));
}

struct VAL_cell* AST_tree_ite(struct AST_tree* self, struct VAL_cell* x, struct AST_tree* ift, struct AST_tree* iff, struct VAL_env* environ)
{
    if(!(x->type == BOOL))
    {
        AST_tree_error(self, "invalid type (1st argument : BOOL) ");
        return NULL;
    }

    if(x->intval)
    {
        return AST_tree_eval(ift, environ);
    }
    else
    {
        return AST_tree_eval(iff, environ);
    }
}

struct VAL_cell* AST_tree_fun(struct AST_tree* self, struct VAL_cell* x, struct AST_tree* body, struct VAL_env* environ)
{
    return new_FUNC_VAL_cell(x,body,environ);
}

struct VAL_cell* AST_tree_concat(struct AST_tree* self, struct VAL_cell* x, struct VAL_cell* y)
{
    if(!(x->type == STRING && y->type == STRING))
    {
        AST_tree_error(self, "invalid type (STRING) ");
        return NULL;
    }
    unsigned int lenx = strlen(x->strval);
    unsigned int leny = strlen(y->strval);
    char* tmp_val = (char*)malloc(lenx + leny + 1);
    memcpy(tmp_val, x->strval, lenx);
    memcpy(tmp_val + lenx, y->strval, leny);
    tmp_val[lenx+leny] = '\x00';
    struct VAL_cell* retval = new_STR_VAL_cell(tmp_val);
    free(tmp_val);
    return retval;

}

struct VAL_cell* AST_tree_subst(struct AST_tree* self, struct VAL_cell* x, struct VAL_cell* y, struct VAL_cell* z)
{
    if(!(x->type == STRING && y->type == INT && z->type == INT))
    {
        AST_tree_error(self, "invalid type (STRING, INT, INT)");
        return NULL;
    }
    long long int spos = y->intval;
    long long int fpos = z->intval;
    if(spos < 0 || fpos < 0)
    {
        AST_tree_error(self, "index must be positive");
        return NULL;
    }
    if(spos > fpos)
    {
        AST_tree_error(self, "start pos <= end pos");
        return NULL;
    }
    if(fpos > strlen(x->strval))
    {
        AST_tree_error(self, "index out of bound");
        return NULL;
    }
    char* tmp_val = (char*) malloc(fpos-spos + 1);
    memcpy(tmp_val, x->strval + spos, fpos-spos);
    tmp_val[fpos-spos] = '\x00';
    struct VAL_cell* retval = new_STR_VAL_cell(tmp_val);
    free(tmp_val);
    return retval;
}

struct VAL_cell* AST_tree_let(struct AST_tree* self, struct VAL_cell* x, struct VAL_cell* y, struct AST_tree* body, struct VAL_env* environ)
{
    struct VAL_env* newe = new_VAL_env(x->strval, y);
    newe->next = VAL_env_deepcopy(environ);
    struct VAL_cell* retval = AST_tree_eval(body, newe);
    del_VAL_env(newe);
    return retval;
}

struct VAL_cell* AST_tree_app(struct AST_tree* self, struct VAL_cell* x, struct VAL_cell* y, struct VAL_env* environ)
{
    if(x->type != FUNC)
    {
        AST_tree_error(self, "cannot apply non-function");
        return NULL;
    }
    struct VAL_env* newe = new_VAL_env(x->left->strval, y);
    newe->next = VAL_env_deepcopy(x->env);
    struct VAL_cell* retval = AST_tree_eval(x->body, newe);
    del_VAL_env(newe);
    return retval;
}


struct VAL_cell* AST_tree_eval(struct AST_tree* self, struct VAL_env* environ)
{
    if(!self)
    {
        AST_tree_error(self, "invalid ast");
        return NULL;
    }
    struct VAL_cell* retval;
    struct VAL_cell* x;
    struct VAL_cell* y;
    struct VAL_cell* z;
    switch(self->type)
    {
        case VAL:
            retval = AST_tree_val(self, self->value, environ);
            break;
        case ADD:
            x = AST_tree_eval(self->leftn, environ);
            if(!x) return NULL;
            y = AST_tree_eval(self->rightn, environ);
            if(!y){
                del_VAL_cell(x);
                return NULL;
            }
            retval = AST_tree_add(self,x,y);
            del_VAL_cell(x);
            del_VAL_cell(y);
            break;
        case SUB:
            x = AST_tree_eval(self->leftn, environ);
            if(!x) return NULL;
            y = AST_tree_eval(self->rightn, environ);
            if(!y) {
                del_VAL_cell(x);
                return NULL;
            }
            retval = AST_tree_sub(self,x,y);
            del_VAL_cell(x);
            del_VAL_cell(y);
            break;
        case MUL:
            x = AST_tree_eval(self->leftn, environ);
            if(!x) return NULL;
            y = AST_tree_eval(self->rightn, environ);
            if(!y) {
                del_VAL_cell(x);
                return NULL;
            }
            retval = AST_tree_mul(self,x,y);
            del_VAL_cell(x);
            del_VAL_cell(y);
            break;
        case CON:
            x = AST_tree_eval(self->leftn, environ);
            if(!x) return NULL;
            y = AST_tree_eval(self->rightn, environ);
            if(!y)
            {
                del_VAL_cell(x);
                return NULL;
            }
            retval = AST_tree_con(self, x, y);
            del_VAL_cell(x);
            del_VAL_cell(y);
            break;
        case CAR:
            x = AST_tree_eval(self->leftn, environ);
            if(!x) return NULL;
            retval = AST_tree_car(self,x);
            del_VAL_cell(x);
            break;
        case CDR:
            x = AST_tree_eval(self->leftn, environ);
            if(!x) return NULL;
            retval = AST_tree_cdr(self, x);
            del_VAL_cell(x);
            break;
        case LT:
            x = AST_tree_eval(self->leftn, environ);
            if(!x) return NULL;
            y = AST_tree_eval(self->rightn, environ);
            if(!y)
            {
                del_VAL_cell(x);
                return NULL;
            }
            retval = AST_tree_lt(self,x,y);
            del_VAL_cell(x);
            del_VAL_cell(y);
            break;
        case GT:
            x = AST_tree_eval(self->leftn, environ);
            if(!x) return NULL;
            y = AST_tree_eval(self->rightn, environ);
            if(!y)
            {
                del_VAL_cell(x);
                return NULL;
            }
            retval = AST_tree_gt(self,x,y);
            del_VAL_cell(x);
            del_VAL_cell(y);
            break;
        case EQ:
            x = AST_tree_eval(self->leftn, environ);
            if(!x) return NULL;
            y = AST_tree_eval(self->rightn, environ);
            if(!y)
            {
                del_VAL_cell(x);
                return NULL;
            }
            retval = AST_tree_eq(self,x, y);
            del_VAL_cell(x);
            del_VAL_cell(y);
            break;
        case OR:
            x = AST_tree_eval(self->leftn, environ);
            if(!x) return NULL;
            y = AST_tree_eval(self->rightn, environ);
            if(!y)
            {
                del_VAL_cell(x);
                return NULL;
            }
            retval = AST_tree_or(self,x,y);
            del_VAL_cell(x);
            del_VAL_cell(y);
            break;
        case AND:
            x = AST_tree_eval(self->leftn, environ);
            if(!x) return NULL;
            y = AST_tree_eval(self->rightn, environ);
            if(!y)
            {
                del_VAL_cell(x);
                return NULL;
            }
            retval = AST_tree_and(self,x,y);
            del_VAL_cell(x);
            del_VAL_cell(y);
            break;
       case NOT:
            x = AST_tree_eval(self->leftn, environ);
            if(!x) return NULL;
            retval = AST_tree_not(self,x);
            del_VAL_cell(x);
            break;
        case ITE:
            x = AST_tree_eval(self->leftn, environ);
            if(!x) return NULL;
            retval = AST_tree_ite(self, x, self->rightn, self->elsen, environ);
            del_VAL_cell(x);
            break;
        case FUN:
            x = AST_tree_sym(self, self->leftn->value);
            if(!x) return NULL;
            retval = AST_tree_fun(self, x, self->rightn, environ);
            del_VAL_cell(x);
            break;
        case CONCAT:
            x = AST_tree_eval(self->leftn, environ);
            if(!x) return NULL;
            y = AST_tree_eval(self->rightn, environ);
            if(!y)
            {
                del_VAL_cell(x);
                return NULL;
            }
            retval = AST_tree_concat(self, x, y);
            del_VAL_cell(x);
            del_VAL_cell(y);
            break;
        case SUBST:
            x = AST_tree_eval(self->leftn, environ);
            if(!x) return NULL;
            y = AST_tree_eval(self->rightn, environ);
            if(!y)
            {
                del_VAL_cell(x);
                return NULL;
            }
            z = AST_tree_eval(self->elsen, environ);
            if(!z)
            {
                del_VAL_cell(x);
                del_VAL_cell(y);
                return NULL;
            }
            retval = AST_tree_subst(self,x,y,z);
            del_VAL_cell(x);
            del_VAL_cell(y);
            del_VAL_cell(z);
            break;
        case LET:
            x = AST_tree_sym(self,self->leftn->value);
            if(!x) return NULL;
            y = AST_tree_eval(self->rightn, environ);
            if(!y)
            {
                del_VAL_cell(x);
                return NULL;
            }
            retval = AST_tree_let(self, x, y, self->elsen, environ);
            del_VAL_cell(x);
            del_VAL_cell(y);
            break;
        case APP:
            x = AST_tree_eval(self->leftn, environ);
            if(!x) return NULL;
            y = AST_tree_eval(self->rightn, environ);
            if(!y)
            {
                del_VAL_cell(x);
                return NULL;
            }
            retval = AST_tree_app(self, x, y, environ);
            del_VAL_cell(x);
            del_VAL_cell(y);
            break;
    }
    return retval;
}
