#ifndef __VALENV__
#define __VALENV__
#include "valcell.h"


struct VAL_env
{
    char val_name[320];
    struct VAL_cell* elem;
    struct VAL_env* next;
};


struct VAL_env* new_VAL_env(char* val_name, struct VAL_cell* elem);

void del_VAL_env(struct VAL_env* self);

struct VAL_env* VAL_env_deepcopy(struct VAL_env* self);

#endif
