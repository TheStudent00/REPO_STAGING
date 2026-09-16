/* probe 678 -- binary << */
#include <stdint.h>
#include <stdbool.h>

__typeof__((int32_t){0} << (int32_t){0})
op_678(int32_t a, int32_t b)
{
    return a << b;
}


uint64_t
emu_RTYPEW__SLLW(uint64_t a, uint64_t b)
{
    return (uint64_t)(op_678(a, b));
}
