/* probe 82 -- unary _Alignof */
#include <stdint.h>
#include <stdbool.h>

__typeof__(_Alignof (double){0})
op_82(double a)
{
    return _Alignof a;
}
