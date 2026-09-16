/* probe 271 -- binary % */
#include <stdint.h>
#include <stdbool.h>

__typeof__((double){0} % (int64_t){0})
op_271(double a, int64_t b)
{
    return a % b;
}
