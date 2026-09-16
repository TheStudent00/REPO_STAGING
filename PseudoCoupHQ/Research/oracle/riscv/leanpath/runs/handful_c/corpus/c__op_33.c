/* probe 33 -- unary & */
#include <stdint.h>
#include <stdbool.h>

__typeof__(&(float){0})
op_33(float a)
{
    return &a;
}
