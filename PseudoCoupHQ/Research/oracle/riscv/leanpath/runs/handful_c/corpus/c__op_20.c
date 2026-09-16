/* probe 20 -- unary + */
#include <stdint.h>
#include <stdbool.h>

__typeof__(+(uint64_t){0})
op_20(uint64_t a)
{
    return +a;
}
