/* probe 310 -- binary || */
#include <stdint.h>
#include <stdbool.h>

__typeof__((double){0} || (double){0})
op_310(double a, double b)
{
    return a || b;
}
