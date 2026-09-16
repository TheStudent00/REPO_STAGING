/* probe 18 -- unary + */
#include <stdint.h>
#include <stdbool.h>

__typeof__(+(int32_t){0})
op_18(int32_t a)
{
    return +a;
}
