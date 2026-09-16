/* probe 118 -- binary + */
#include <stdint.h>
#include <stdbool.h>

__typeof__((uint64_t){0} + (double){0})
op_118(uint64_t a, double b)
{
    return a + b;
}
