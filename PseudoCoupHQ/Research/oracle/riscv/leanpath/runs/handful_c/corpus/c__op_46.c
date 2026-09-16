/* probe 46 -- unary -- */
#include <stdint.h>
#include <stdbool.h>

__typeof__(--(double){0})
op_46(double a)
{
    return --a;
}
