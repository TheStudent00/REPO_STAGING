/* probe 60 -- unary __alignof */
#include <stdint.h>
#include <stdbool.h>

__typeof__(__alignof (int32_t){0})
op_60(int32_t a)
{
    return __alignof a;
}
