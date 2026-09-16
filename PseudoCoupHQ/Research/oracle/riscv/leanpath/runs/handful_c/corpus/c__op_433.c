/* probe 433 -- binary & */
#include <stdint.h>
#include <stdbool.h>

__typeof__((int64_t){0} & (int64_t){0})
op_433(int64_t a, int64_t b)
{
    return a & b;
}
