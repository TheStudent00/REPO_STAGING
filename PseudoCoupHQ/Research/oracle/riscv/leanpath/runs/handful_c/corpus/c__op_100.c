/* probe 100 -- unary -- */
#include <stdint.h>
#include <stdbool.h>

__typeof__((double){0}--)
op_100(double a)
{
    return a--;
}
