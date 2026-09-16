/* probe 728 -- binary >> */
#include <stdint.h>
#include <stdbool.h>

__typeof__((uint64_t){0} >> (uint64_t){0})
op_728(uint64_t a, uint64_t b)
{
    return a >> b;
}


uint64_t
emu_RTYPE__SRL(uint64_t a, uint64_t b)
{
    return (uint64_t)(op_728(a, b));
}
