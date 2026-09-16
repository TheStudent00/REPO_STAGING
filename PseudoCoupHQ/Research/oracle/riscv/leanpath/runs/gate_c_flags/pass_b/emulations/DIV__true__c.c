/* probe 218 -- binary / */
#include <stdint.h>
#include <stdbool.h>

__typeof__((int64_t){0} / (uint64_t){0})
op_218(int64_t a, uint64_t b)
{
    return a / b;
}


uint64_t
emu_DIV__true(uint64_t a, uint64_t b)
{
    return (uint64_t)(op_218(a, b));
}
