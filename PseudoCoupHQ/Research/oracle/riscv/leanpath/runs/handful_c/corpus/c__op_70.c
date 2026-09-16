/* probe 70 -- unary _alignof */
#include <stdint.h>
#include <stdbool.h>

__typeof__(_alignof (double){0})
op_70(double a)
{
    return _alignof a;
}
