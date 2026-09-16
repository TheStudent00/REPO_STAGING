/* probe 14 -- unary - */
#include <stdint.h>
#include <stdbool.h>

__typeof__(-(uint64_t){0})
op_14(uint64_t a)
{
    return -a;
}
