/* probe 81 -- unary _Alignof */
#include <stdint.h>
#include <stdbool.h>

__typeof__(_Alignof (float){0})
op_81(float a)
{
    return _Alignof a;
}
