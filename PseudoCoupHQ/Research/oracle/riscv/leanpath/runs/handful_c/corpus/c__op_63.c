/* probe 63 -- unary __alignof */
#include <stdint.h>
#include <stdbool.h>

__typeof__(__alignof (float){0})
op_63(float a)
{
    return __alignof a;
}
