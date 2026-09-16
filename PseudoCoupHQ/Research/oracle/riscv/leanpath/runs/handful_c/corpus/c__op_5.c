/* probe 5 -- unary ! */
#include <stdint.h>
#include <stdbool.h>

__typeof__(!(bool){0})
op_5(bool a)
{
    return !a;
}
