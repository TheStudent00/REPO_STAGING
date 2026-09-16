/* probe 237 -- binary / */
#include <stdint.h>
#include <stdbool.h>

__typeof__((double){0} / (float){0})
op_237(double a, float b)
{
    return a / b;
}
