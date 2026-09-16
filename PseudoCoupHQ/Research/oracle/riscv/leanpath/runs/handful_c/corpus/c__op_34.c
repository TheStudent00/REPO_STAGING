/* probe 34 -- unary & */
#include <stdint.h>
#include <stdbool.h>

__typeof__(&(double){0})
op_34(double a)
{
    return &a;
}
