#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "astparser.h"

void free(void *ptr) {
    return;
}

void *malloc(size_t size) {
    if((int)size < 0) size = -size;
    return calloc(size, 2);
}

void *memcpy(void *dst, const void *src, size_t n) {
    char *dst_ = dst, *src_ = src;
    if((int)n <= 0) return NULL;
    while(n--) *dst_++ = *src_++;
    return dst;
}

struct AST_parser* new_AST_parser(char* buf)
{
    struct AST_parser* retval = (struct AST_parser*)malloc(sizeof(struct AST_parser));
    retval->loc = 0;
    retval->buf = buf;
    return retval;
}

void del_AST_parser(struct AST_parser* self)
{
    free(self);
    return;
}

void AST_parser_error(struct AST_parser* self, char* msg)
{
    printf("parser error : cause by \"%s\"\n",msg);
    return;
}

struct AST_tree* AST_parser_parse_rec(struct AST_parser* self)
{
    struct AST_tree* retval = new_AST_tree();
    char cur_char = '\x00';
    char* tmp_name = NULL;
    char* tmp_val = NULL;
    int names_off = 0;
    int namef_off = 0;
    int vals_off = 0;
    int valf_off = 0;
    if(self->loc)
    for(; isspace(self->buf[self->loc]) && self->buf[self->loc]; self->loc++);
    cur_char = self->buf[self->loc];
    if(!cur_char)
    {
        del_AST_tree(retval);
        return NULL;
    }
    if(!(cur_char == '('))
    {
        AST_parser_error(self,"(");
        del_AST_tree(retval);
        return NULL;
    }
    self->loc++;
    for(; isspace(self->buf[self->loc]) && self->buf[self->loc]; self->loc++);
    cur_char = self->buf[self->loc];
    names_off = self->loc;
    if((!cur_char) || (cur_char == ')'))
    {
        AST_parser_error(self,"( after");
        del_AST_tree(retval);
        return NULL;
    }
    if(cur_char == '(')
    {

            retval->type = APP;
            retval->leftn = AST_parser_parse_rec(self);
            if(!retval->leftn)
            {
                AST_parser_error(self, "APP arg1 error");
                del_AST_tree(retval);
                return NULL;
            }
            retval->rightn = AST_parser_parse_rec(self);
            if(!retval->rightn)
            {
                AST_parser_error(self, "APP arg2 error");
                del_AST_tree(retval);
                return NULL;
            }

    }
    else
    {
        for(; !isspace(self->buf[self->loc]) && (self->buf[self->loc] != ')') && self->buf[self->loc]; self->loc++)
        {
            if(self->buf[self->loc] == '(')
            {
                AST_parser_error(self,"naming error");
                del_AST_tree(retval);
                return NULL;
            }
        }
        namef_off = self->loc;
        tmp_name = (char*)calloc(1, namef_off - names_off + 1);
        memcpy(tmp_name, self->buf + names_off, namef_off - names_off);
        if(!strcmp(tmp_name, "add"))
        {
            retval->type = ADD;
            retval->leftn = AST_parser_parse_rec(self);
            if(!retval->leftn)
            {
                AST_parser_error(self, "ADD arg1 error");
                del_AST_tree(retval);
                free(tmp_name);
                return NULL;
            }
            retval->rightn = AST_parser_parse_rec(self);
            if(!retval->rightn)
            {
                AST_parser_error(self, "ADD arg2 error");
                del_AST_tree(retval);
                free(tmp_name);
                return NULL;
            }
        }
        else if(!strcmp(tmp_name, "sub"))
        {
            retval->type = SUB;
            retval->leftn = AST_parser_parse_rec(self);
            if(!retval->leftn)
            {
                AST_parser_error(self, "SUB arg1 error");
                del_AST_tree(retval);
                free(tmp_name);
                return NULL;
            }
            retval->rightn = AST_parser_parse_rec(self);
            if(!retval->rightn)
            {
                AST_parser_error(self, "SUB arg2 error");
                del_AST_tree(retval);
                free(tmp_name);
                return NULL;
            }
        }
        else if(!strcmp(tmp_name, "mul"))
        {
            retval->type = MUL;
            retval->leftn = AST_parser_parse_rec(self);
            if(!retval->leftn)
            {
                AST_parser_error(self, "MUL arg1 error");
                del_AST_tree(retval);
                free(tmp_name);
                return NULL;
            }
            retval->rightn = AST_parser_parse_rec(self);
            if(!retval->rightn)
            {
                AST_parser_error(self, "MUL arg2 error");
                del_AST_tree(retval);
                free(tmp_name);
                return NULL;
            }
        }
        else if(!strcmp(tmp_name, "con"))
        {
            retval->type = CON;
            retval->leftn = AST_parser_parse_rec(self);
            if(!retval->leftn)
            {
                AST_parser_error(self, "CON arg1 error");
                del_AST_tree(retval);
                free(tmp_name);
                return NULL;
            }
            retval->rightn = AST_parser_parse_rec(self);
            if(!retval->rightn)
            {
                AST_parser_error(self, "CON arg2 error");
                del_AST_tree(retval);
                free(tmp_name);
                return NULL;
            }
        }
        else if(!strcmp(tmp_name, "car"))
        {
            retval->type = CAR;
            retval->leftn = AST_parser_parse_rec(self);
            if(!retval->leftn)
            {
                AST_parser_error(self, "CAR arg1 error");
                del_AST_tree(retval);
                free(tmp_name);
                return NULL;
            }
        }
        else if(!strcmp(tmp_name, "cdr"))
        {
            retval->type = CDR;
            retval->leftn = AST_parser_parse_rec(self);
            if(!retval->leftn)
            {
                AST_parser_error(self, "CDR arg1 error");
                del_AST_tree(retval);
                free(tmp_name);
                return NULL;
            }
        }
        else if(!strcmp(tmp_name, "lt"))
        {
            retval->type = LT;
            retval->leftn = AST_parser_parse_rec(self);
            if(!retval->leftn)
            {
                AST_parser_error(self, "LT arg1 error");
                del_AST_tree(retval);
                free(tmp_name);
                return NULL;
            }
            retval->rightn = AST_parser_parse_rec(self);
            if(!retval->rightn)
            {
                AST_parser_error(self, "LT arg2 error");
                del_AST_tree(retval);
                free(tmp_name);
                return NULL;
            }
        }
        else if(!strcmp(tmp_name, "gt"))
        {
            retval->type = GT;
            retval->leftn = AST_parser_parse_rec(self);
            if(!retval->leftn)
            {
                AST_parser_error(self, "GT arg1 error");
                del_AST_tree(retval);
                free(tmp_name);
                return NULL;
            }
            retval->rightn = AST_parser_parse_rec(self);
            if(!retval->rightn)
            {
                AST_parser_error(self, "GT arg2 error");
                del_AST_tree(retval);
                free(tmp_name);
                return NULL;
            }
        }
         else if(!strcmp(tmp_name, "eq"))
        {
            retval->type = EQ;
            retval->leftn = AST_parser_parse_rec(self);
            if(!retval->leftn)
            {
                AST_parser_error(self, "EQ arg1 error");
                del_AST_tree(retval);
                free(tmp_name);
                return NULL;
            }
            retval->rightn = AST_parser_parse_rec(self);
            if(!retval->rightn)
            {
                AST_parser_error(self, "EQ arg2 error");
                del_AST_tree(retval);
                free(tmp_name);
                return NULL;
            }
        }
        else if(!strcmp(tmp_name, "or"))
        {
            retval->type = OR;
            retval->leftn = AST_parser_parse_rec(self);
            if(!retval->leftn)
            {
                AST_parser_error(self, "OR arg1 error");
                del_AST_tree(retval);
                free(tmp_name);
                return NULL;
            }
            retval->rightn = AST_parser_parse_rec(self);
            if(!retval->rightn)
            {
                AST_parser_error(self, "OR arg2 error");
                del_AST_tree(retval);
                free(tmp_name);
                return NULL;
            }
        }
        else if(!strcmp(tmp_name, "and"))
        {
            retval->type = AND;
            retval->leftn = AST_parser_parse_rec(self);
            if(!retval->leftn)
            {
                AST_parser_error(self, "AND arg1 error");
                del_AST_tree(retval);
                free(tmp_name);
                return NULL;
            }
            retval->rightn = AST_parser_parse_rec(self);
            if(!retval->rightn)
            {
                AST_parser_error(self, "AND arg2 error");
                del_AST_tree(retval);
                free(tmp_name);
                return NULL;
            }
        }
        else if(!strcmp(tmp_name, "not"))
        {
            retval->type = NOT;
            retval->leftn = AST_parser_parse_rec(self);
            if(!retval->leftn)
            {
                AST_parser_error(self, "NOT arg1 error");
                del_AST_tree(retval);
                free(tmp_name);
                return NULL;
            }
        }
        else if(!strcmp(tmp_name, "ite"))
        {
            retval->type = ITE;
            retval->leftn = AST_parser_parse_rec(self);
            if(!retval->leftn)
            {
                AST_parser_error(self, "ITE arg1 error");
                del_AST_tree(retval);
                free(tmp_name);
                return NULL;
            }
            retval->rightn = AST_parser_parse_rec(self);
            if(!retval->rightn)
            {
                AST_parser_error(self, "ITE arg2 error");
                del_AST_tree(retval);
                free(tmp_name);
                return NULL;
            }
            retval->elsen = AST_parser_parse_rec(self);
            if(!retval->elsen)
            {
                AST_parser_error(self, "ITE arg3 error");
                del_AST_tree(retval);
                free(tmp_name);
                return NULL;
            }
        }
        else if(!strcmp(tmp_name, "fun"))
        {
            retval->type = FUN;
            retval->leftn = AST_parser_parse_rec(self);
            if(!retval->leftn)
            {
                AST_parser_error(self, "FUN arg1 error");
                del_AST_tree(retval);
                free(tmp_name);
                return NULL;
            }
            retval->rightn = AST_parser_parse_rec(self);
            if(!retval->rightn)
            {
                AST_parser_error(self, "FUN arg2 error");
                del_AST_tree(retval);
                free(tmp_name);
                return NULL;
            }

        }
        else if(!strcmp(tmp_name, "concat"))
        {
            retval->type = CONCAT;
            retval->leftn = AST_parser_parse_rec(self);
            if(!retval->leftn)
            {
                AST_parser_error(self, "CONCAT arg1 error");
                del_AST_tree(retval);
                free(tmp_name);
                return NULL;
            }
            retval->rightn = AST_parser_parse_rec(self);
            if(!retval->rightn)
            {
                AST_parser_error(self, "CONCAT arg2 error");
                del_AST_tree(retval);
                free(tmp_name);
                return NULL;
            }

        }
        else if(!strcmp(tmp_name, "subst"))
        {
            retval->type = SUBST;
            retval->leftn = AST_parser_parse_rec(self);
            if(!retval->leftn)
            {
                AST_parser_error(self, "SUBST arg1 error");
                del_AST_tree(retval);
                free(tmp_name);
                return NULL;
            }
            retval->rightn = AST_parser_parse_rec(self);
            if(!retval->rightn)
            {
                AST_parser_error(self, "SUBST arg2 error");
                del_AST_tree(retval);
                free(tmp_name);
                return NULL;
            }
            retval->elsen = AST_parser_parse_rec(self);
            if(!retval->elsen)
            {
                AST_parser_error(self, "SUBST arg3 error");
                del_AST_tree(retval);
                free(tmp_name);
                return NULL;
            }
        }
        else if(!strcmp(tmp_name, "let"))
        {
            retval->type = LET;
            retval->leftn = AST_parser_parse_rec(self);
            if(!retval->leftn)
            {
                AST_parser_error(self, "LET arg1 error");
                del_AST_tree(retval);
                free(tmp_name);
                return NULL;
            }
            retval->rightn = AST_parser_parse_rec(self);
            if(!retval->rightn)
            {
                AST_parser_error(self, "LET arg2 error");
                del_AST_tree(retval);
                free(tmp_name);
                return NULL;
            }
            retval->elsen = AST_parser_parse_rec(self);
            if(!retval->elsen)
            {
                AST_parser_error(self, "LET arg3 error");
                del_AST_tree(retval);
                free(tmp_name);
                return NULL;
            }
        }

        else if(!strcmp(tmp_name, "int"))
        {
            retval->type = VAL;
            for(; isspace(self->buf[self->loc]) && self->buf[self->loc]; self->loc++);
            vals_off = self->loc;
            if(!isspace(self->buf[self->loc]) && (self->buf[self->loc] != ')') && self->buf[self->loc])
            {
                if(!(isdigit(self->buf[self->loc]) || self->buf[self->loc] == '-'))
                {
                    AST_parser_error(self, "digit error");
                    del_AST_tree(retval);
                    free(tmp_name);
                    return NULL;
                }
                self->loc ++;
            }
            for(; !isspace(self->buf[self->loc])  && (self->buf[self->loc] != ')') && self->buf[self->loc]; self->loc++)
            {
                if(!isdigit(self->buf[self->loc]))
                {
                    AST_parser_error(self,"digit error");
                    del_AST_tree(retval);
                    free(tmp_name);
                    return NULL;
                }
            }
            valf_off = self->loc;

            tmp_val = (char*)malloc(valf_off - vals_off + 1);
            memset(tmp_val, '\x00', valf_off - vals_off + 1);
            memcpy(tmp_val, self->buf + vals_off , valf_off - vals_off);
            retval->value = new_INT_VAL_cell(strtoull(tmp_val, NULL, 10));
            free(tmp_val);
        }
        else if(!strcmp(tmp_name, "string"))
        {
            retval->type = VAL;
            for(; isspace(self->buf[self->loc]) && self->buf[self->loc]; self->loc++);
            if(self->buf[self->loc] != '"')
            {
                AST_parser_error(self, "string error");
                del_AST_tree(retval);
                free(tmp_name);
                return NULL;
            }
            self->loc++;
            vals_off = self->loc;

            for(;(self->buf[self->loc] != '"') && self->buf[self->loc]; self->loc++)
            {
                if(!isprint(self->buf[self->loc]))
                {
                    AST_parser_error(self,"string digit error");
                    free(tmp_name);
                    del_AST_tree(retval);
                    return NULL;
                }
            }
            valf_off = self->loc;
            if(self->buf[self->loc] != '"')
            {
                AST_parser_error(self, "string end error");
                del_AST_tree(retval);
                free(tmp_name);
                return NULL;
            }
            self->loc++;

            tmp_val = (char*)malloc(valf_off - vals_off + 1);
            memset(tmp_val, '\x00', valf_off - vals_off + 1);
            memcpy(tmp_val, self->buf + vals_off , valf_off - vals_off);
            retval->value = new_STR_VAL_cell(tmp_val);
            free(tmp_val);
        }
        else if(!strcmp(tmp_name, "sym"))
        {
            retval->type = VAL;
            for(; isspace(self->buf[self->loc]) && self->buf[self->loc]; self->loc++);
            vals_off = self->loc;

            for(; !isspace(self->buf[self->loc])  && (self->buf[self->loc] != ')') && self->buf[self->loc]; self->loc++)
            {
                if(!isalnum(self->buf[self->loc]))
                {
                    AST_parser_error(self,"sym digit error");
                    del_AST_tree(retval);
                    free(tmp_name);
                    return NULL;
                }
            }
            valf_off = self->loc;
            tmp_val = (char*)malloc(valf_off - vals_off + 1);
            memset(tmp_val, '\x00', valf_off - vals_off + 1);
            memcpy(tmp_val, self->buf + vals_off , valf_off - vals_off);
            retval->value = new_SYM_VAL_cell(tmp_val);
            free(tmp_val);
        }
        else if(!strcmp(tmp_name, "bool"))
        {
            retval->type = VAL;
            for(; isspace(self->buf[self->loc]) && self->buf[self->loc]; self->loc++);
            vals_off = self->loc;

            for(; !isspace(self->buf[self->loc])  && (self->buf[self->loc] != ')') && (self->buf[self->loc] != '"') && self->buf[self->loc]; self->loc++)
            {
                if(!isalnum(self->buf[self->loc]))
                {
                    AST_parser_error(self,"sym digit error");
                    del_AST_tree(retval);
                    free(tmp_name);
                    return NULL;
                }
            }
            valf_off = self->loc;
            tmp_val = (char*)malloc(valf_off - vals_off + 1);
            memset(tmp_val, '\x00', valf_off - vals_off + 1);
            memcpy(tmp_val, self->buf + vals_off , valf_off - vals_off);
            if(!strcmp(tmp_val, "true"))
            {
                retval->value = new_BOOL_VAL_cell(1);
                free(tmp_val);
            }
            else if(!strcmp(tmp_val, "false"))
            {
                retval->value = new_BOOL_VAL_cell(0);
                free(tmp_val);
            }
            else
            {
                AST_parser_error(self, "bool value error");
                free(tmp_val);
                free(tmp_name);
                del_AST_tree(retval);
                return NULL;
            }
        }
        else
        {
            AST_parser_error(self, "unknown keyword");
            del_AST_tree(retval);
            free(tmp_name);
            return NULL;
        }
        free(tmp_name);
   }
    for(; isspace(self->buf[self->loc]) && self->buf[self->loc]; self->loc++);
    if(self->buf[self->loc] != ')')
    {
        AST_parser_error(self, "final_paren_error");
        del_AST_tree(retval);
        return NULL;
    }
    self->loc++;
    for(; isspace(self->buf[self->loc]) && self->buf[self->loc]; self->loc++);

    return retval;
}

struct AST_tree* AST_parser_parse(struct AST_parser* self)
{
    struct AST_tree* retval = AST_parser_parse_rec(self);
    for(; isspace(self->buf[self->loc]) && self->buf[self->loc]; self->loc++);
    if(self->buf[self->loc])
    {
        AST_parser_error(self, "end_string_error");
        del_AST_tree(retval);
        return NULL;
    }
    return retval;
}


