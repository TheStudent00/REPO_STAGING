/* probe 50 -- unary sizeof */
#include <stdint.h>
#include <stdbool.h>

__typeof__(sizeof (uint64_t){0})
op_50(uint64_t a)
{
    return sizeof a;
}
