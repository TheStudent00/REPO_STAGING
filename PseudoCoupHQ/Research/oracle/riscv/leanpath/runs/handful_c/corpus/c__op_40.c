/* probe 40 -- unary ++ */
#include <stdint.h>
#include <stdbool.h>

__typeof__(++(double){0})
op_40(double a)
{
    return ++a;
}
