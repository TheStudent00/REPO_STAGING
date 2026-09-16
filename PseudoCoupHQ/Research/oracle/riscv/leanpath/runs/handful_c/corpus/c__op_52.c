/* probe 52 -- unary sizeof */
#include <stdint.h>
#include <stdbool.h>

__typeof__(sizeof (double){0})
op_52(double a)
{
    return sizeof a;
}
