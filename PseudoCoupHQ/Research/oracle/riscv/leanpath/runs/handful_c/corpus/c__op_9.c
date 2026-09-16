/* probe 9 -- unary ~ */
#include <stdint.h>
#include <stdbool.h>

__typeof__(~(float){0})
op_9(float a)
{
    return ~a;
}
