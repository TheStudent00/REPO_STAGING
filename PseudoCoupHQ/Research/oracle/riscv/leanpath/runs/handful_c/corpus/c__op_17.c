/* probe 17 -- unary - */
#include <stdint.h>
#include <stdbool.h>

__typeof__(-(bool){0})
op_17(bool a)
{
    return -a;
}
