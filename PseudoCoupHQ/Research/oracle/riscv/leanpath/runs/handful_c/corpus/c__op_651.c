/* probe 651 -- binary < */
#include <stdint.h>
#include <stdbool.h>

__typeof__((int64_t){0} < (float){0})
op_651(int64_t a, float b)
{
    return a < b;
}
