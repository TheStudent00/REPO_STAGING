/* probe 56 -- unary __alignof__ */
#include <stdint.h>
#include <stdbool.h>

__typeof__(__alignof__ (uint64_t){0})
op_56(uint64_t a)
{
    return __alignof__ a;
}
