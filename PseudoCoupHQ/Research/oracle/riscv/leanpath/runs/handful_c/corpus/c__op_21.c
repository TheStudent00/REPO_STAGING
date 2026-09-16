/* probe 21 -- unary + */
#include <stdint.h>
#include <stdbool.h>

__typeof__(+(float){0})
op_21(float a)
{
    return +a;
}
