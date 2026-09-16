/* probe 53 -- unary sizeof */
#include <stdint.h>
#include <stdbool.h>

__typeof__(sizeof (bool){0})
op_53(bool a)
{
    return sizeof a;
}
