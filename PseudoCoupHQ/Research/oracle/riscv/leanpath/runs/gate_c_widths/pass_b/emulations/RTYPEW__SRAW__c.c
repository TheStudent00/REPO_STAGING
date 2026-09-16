/* probe 714 -- binary >> */
#include <stdint.h>
#include <stdbool.h>

__typeof__((int32_t){0} >> (int32_t){0})
op_714(int32_t a, int32_t b)
{
    return a >> b;
}


uint64_t
emu_RTYPEW__SRAW(uint64_t a, uint64_t b)
{
    return (uint64_t)(op_714(a, b));
}
