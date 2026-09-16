/* probe 144 -- binary - */
#include <stdint.h>
#include <stdbool.h>

__typeof__((int64_t){0} - (int32_t){0})
op_144(int64_t a, int32_t b)
{
    return a - b;
}


uint64_t
emu_RTYPE__SUB(uint64_t a, uint64_t b)
{
    return (uint64_t)(op_144(a, b));
}
