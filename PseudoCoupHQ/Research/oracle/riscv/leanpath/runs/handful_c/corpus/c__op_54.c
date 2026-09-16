/* probe 54 -- unary __alignof__ */
#include <stdint.h>
#include <stdbool.h>

__typeof__(__alignof__ (int32_t){0})
op_54(int32_t a)
{
    return __alignof__ a;
}
