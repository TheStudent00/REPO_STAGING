/* probe 28 -- unary * */
#include <stdint.h>
#include <stdbool.h>

__typeof__(*(double){0})
op_28(double a)
{
    return *a;
}
