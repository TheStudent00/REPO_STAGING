/* probe 42 -- unary -- */
#include <stdint.h>
#include <stdbool.h>

__typeof__(--(int32_t){0})
op_42(int32_t a)
{
    return --a;
}
