/* probe 400 -- binary ^ */
#include <stdint.h>
#include <stdbool.h>

__typeof__((int64_t){0} ^ (double){0})
op_400(int64_t a, double b)
{
    return a ^ b;
}
