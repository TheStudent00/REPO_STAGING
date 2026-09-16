/* probe 721 -- binary >> */
#include <stdint.h>
#include <stdbool.h>

__typeof__((int64_t){0} >> (int64_t){0})
op_721(int64_t a, int64_t b)
{
    return a >> b;
}


uint64_t
emu_RTYPE__SRA(uint64_t a, uint64_t b)
{
    return (uint64_t)(op_721(a, b));
}
