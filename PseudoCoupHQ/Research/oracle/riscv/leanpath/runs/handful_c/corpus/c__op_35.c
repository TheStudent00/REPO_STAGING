/* probe 35 -- unary & */
#include <stdint.h>
#include <stdbool.h>

__typeof__(&(bool){0})
op_35(bool a)
{
    return &a;
}
