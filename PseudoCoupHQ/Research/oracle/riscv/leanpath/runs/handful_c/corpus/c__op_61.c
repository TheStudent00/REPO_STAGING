/* probe 61 -- unary __alignof */
#include <stdint.h>
#include <stdbool.h>

__typeof__(__alignof (int64_t){0})
op_61(int64_t a)
{
    return __alignof a;
}
