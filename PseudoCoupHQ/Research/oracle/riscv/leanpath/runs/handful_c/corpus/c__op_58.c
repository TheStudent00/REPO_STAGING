/* probe 58 -- unary __alignof__ */
#include <stdint.h>
#include <stdbool.h>

__typeof__(__alignof__ (double){0})
op_58(double a)
{
    return __alignof__ a;
}
