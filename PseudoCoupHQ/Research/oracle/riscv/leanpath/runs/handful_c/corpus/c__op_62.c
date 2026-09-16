/* probe 62 -- unary __alignof */
#include <stdint.h>
#include <stdbool.h>

__typeof__(__alignof (uint64_t){0})
op_62(uint64_t a)
{
    return __alignof a;
}
