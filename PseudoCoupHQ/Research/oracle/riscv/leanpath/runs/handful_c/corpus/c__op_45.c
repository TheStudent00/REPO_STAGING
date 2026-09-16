/* probe 45 -- unary -- */
#include <stdint.h>
#include <stdbool.h>

__typeof__(--(float){0})
op_45(float a)
{
    return --a;
}
