/* probe 49 -- unary sizeof */
#include <stdint.h>
#include <stdbool.h>

__typeof__(sizeof (int64_t){0})
op_49(int64_t a)
{
    return sizeof a;
}
