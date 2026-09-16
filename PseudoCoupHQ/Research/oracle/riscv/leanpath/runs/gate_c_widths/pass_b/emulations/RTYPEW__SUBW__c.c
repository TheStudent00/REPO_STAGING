/* probe 138 -- binary - */
#include <stdint.h>
#include <stdbool.h>

__typeof__((int32_t){0} - (int32_t){0})
op_138(int32_t a, int32_t b)
{
    return a - b;
}


uint64_t
emu_RTYPEW__SUBW(uint64_t a, uint64_t b)
{
    return (uint64_t)(op_138(a, b));
}
