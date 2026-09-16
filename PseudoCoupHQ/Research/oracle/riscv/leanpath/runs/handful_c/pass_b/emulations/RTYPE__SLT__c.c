/* probe 649 -- binary < */
#include <stdint.h>
#include <stdbool.h>

__typeof__((int64_t){0} < (int64_t){0})
op_649(int64_t a, int64_t b)
{
    return a < b;
}


uint64_t
emu_RTYPE__SLT(uint64_t a, uint64_t b)
{
    return (uint64_t)(op_649(a, b));
}
