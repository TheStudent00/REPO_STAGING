/* probe 253 -- binary % */
#include <stdint.h>
#include <stdbool.h>

__typeof__((int64_t){0} % (int64_t){0})
op_253(int64_t a, int64_t b)
{
    return a % b;
}


uint64_t
emu_REM__false(uint64_t a, uint64_t b)
{
    return (uint64_t)(op_253(a, b));
}
