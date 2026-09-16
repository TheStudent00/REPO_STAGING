/* probe 10 -- unary ~ */
#include <stdint.h>
#include <stdbool.h>

__typeof__(~(double){0})
op_10(double a)
{
    return ~a;
}
