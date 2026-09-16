/* probe 64 -- unary __alignof */
#include <stdint.h>
#include <stdbool.h>

__typeof__(__alignof (double){0})
op_64(double a)
{
    return __alignof a;
}
