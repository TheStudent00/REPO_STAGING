/* probe 48 -- unary sizeof */
#include <stdint.h>
#include <stdbool.h>

__typeof__(sizeof (int32_t){0})
op_48(int32_t a)
{
    return sizeof a;
}
