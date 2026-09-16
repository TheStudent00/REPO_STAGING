/* probe 57 -- unary __alignof__ */
#include <stdint.h>
#include <stdbool.h>

__typeof__(__alignof__ (float){0})
op_57(float a)
{
    return __alignof__ a;
}
