/* probe 417 -- binary ^ */
#include <stdint.h>
#include <stdbool.h>

__typeof__((double){0} ^ (float){0})
op_417(double a, float b)
{
    return a ^ b;
}
