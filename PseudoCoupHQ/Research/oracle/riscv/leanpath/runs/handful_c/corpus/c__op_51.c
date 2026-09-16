/* probe 51 -- unary sizeof */
#include <stdint.h>
#include <stdbool.h>

__typeof__(sizeof (float){0})
op_51(float a)
{
    return sizeof a;
}
