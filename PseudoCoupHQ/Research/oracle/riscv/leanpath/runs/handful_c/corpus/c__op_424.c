/* probe 424 -- binary ^ */
#include <stdint.h>
#include <stdbool.h>

__typeof__((bool){0} ^ (double){0})
op_424(bool a, double b)
{
    return a ^ b;
}
