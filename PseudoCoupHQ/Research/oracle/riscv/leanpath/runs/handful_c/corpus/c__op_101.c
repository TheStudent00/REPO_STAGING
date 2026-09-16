/* probe 101 -- unary -- */
#include <stdint.h>
#include <stdbool.h>

__typeof__((bool){0}--)
op_101(bool a)
{
    return a--;
}
