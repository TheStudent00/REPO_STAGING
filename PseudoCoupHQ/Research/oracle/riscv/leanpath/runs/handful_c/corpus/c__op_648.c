/* probe 648 -- binary < */
#include <stdint.h>
#include <stdbool.h>

__typeof__((int64_t){0} < (int32_t){0})
op_648(int64_t a, int32_t b)
{
    return a < b;
}
