/* probe 59 -- unary __alignof__ */
#include <stdint.h>
#include <stdbool.h>

__typeof__(__alignof__ (bool){0})
op_59(bool a)
{
    return __alignof__ a;
}
