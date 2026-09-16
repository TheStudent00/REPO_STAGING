/* probe 39 -- unary ++ */
#include <stdint.h>
#include <stdbool.h>

__typeof__(++(float){0})
op_39(float a)
{
    return ++a;
}
