/* probe 662 -- binary < */
#include <stdint.h>
#include <stdbool.h>

__typeof__((float){0} < (uint64_t){0})
op_662(float a, uint64_t b)
{
    return a < b;
}
