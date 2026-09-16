/* probe 13 -- unary - */
#include <stdint.h>
#include <stdbool.h>

__typeof__(-(int64_t){0})
op_13(int64_t a)
{
    return -a;
}
