/* probe 666 -- binary < */
#include <stdint.h>
#include <stdbool.h>

__typeof__((double){0} < (int32_t){0})
op_666(double a, int32_t b)
{
    return a < b;
}
