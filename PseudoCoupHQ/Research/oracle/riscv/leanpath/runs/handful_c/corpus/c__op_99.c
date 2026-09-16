/* probe 99 -- unary -- */
#include <stdint.h>
#include <stdbool.h>

__typeof__((float){0}--)
op_99(float a)
{
    return a--;
}
