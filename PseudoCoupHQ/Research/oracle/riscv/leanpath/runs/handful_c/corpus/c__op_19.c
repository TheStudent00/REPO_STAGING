/* probe 19 -- unary + */
#include <stdint.h>
#include <stdbool.h>

__typeof__(+(int64_t){0})
op_19(int64_t a)
{
    return +a;
}
