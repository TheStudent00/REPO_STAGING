/* probe 8 -- unary ~ */
#include <stdint.h>
#include <stdbool.h>

__typeof__(~(uint64_t){0})
op_8(uint64_t a)
{
    return ~a;
}
