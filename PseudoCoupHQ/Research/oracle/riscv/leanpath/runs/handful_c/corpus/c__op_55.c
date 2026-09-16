/* probe 55 -- unary __alignof__ */
#include <stdint.h>
#include <stdbool.h>

__typeof__(__alignof__ (int64_t){0})
op_55(int64_t a)
{
    return __alignof__ a;
}
