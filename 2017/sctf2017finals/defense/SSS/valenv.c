#include "valenv.h"
#include <stdlib.h>
#include <string.h>


struct VAL_env* new_VAL_env(char* val_name, struct VAL_cell* elem)
{
    struct VAL_env* self = (struct VAL_env*)malloc(sizeof(struct VAL_env));
    self->elem = VAL_cell_deepcopy(elem);
    strncpy(self->val_name, val_name, 32);
    self->next = NULL;
    return self;
}

void del_VAL_env(struct VAL_env* self)
{
    if(!self) return;
    del_VAL_cell(self->elem);
    free(self);
}

struct VAL_env* VAL_env_deepcopy(struct VAL_env* self)
{
    if(!self) return NULL;
    struct VAL_env* retval = new_VAL_env(self->val_name, self->elem);
    retval->next = VAL_env_deepcopy(self->next);
    return retval;
}
