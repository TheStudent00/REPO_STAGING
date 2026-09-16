/* probe 76 -- unary alignof */
#include <stdint.h>
#include <stdbool.h>

__typeof__(alignof (double){0})
op_76(double a)
{
    return alignof a;
}
