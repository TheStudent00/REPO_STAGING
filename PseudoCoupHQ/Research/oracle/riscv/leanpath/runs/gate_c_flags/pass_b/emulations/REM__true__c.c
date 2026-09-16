/* probe 254 -- binary % */
#include <stdint.h>
#include <stdbool.h>

__typeof__((int64_t){0} % (uint64_t){0})
op_254(int64_t a, uint64_t b)
{
    return a % b;
}


uint64_t
emu_REM__true(uint64_t a, uint64_t b)
{
    return (uint64_t)(op_254(a, b));
}
