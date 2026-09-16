/* probe 728 -- binary >> */
#include <stdint.h>
#include <stdbool.h>

__typeof__((uint64_t){0} >> (uint64_t){0})
op_728(uint64_t a, uint64_t b)
{
    return a >> b;
}


uint64_t
emu_SHIFTIOP__SRLI(uint64_t a, uint64_t shamt)
{
    return (uint64_t)(op_728(a, shamt));
}
