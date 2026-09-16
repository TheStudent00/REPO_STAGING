/* probe 404 -- binary ^ */
#include <stdint.h>
#include <stdbool.h>

__typeof__((uint64_t){0} ^ (uint64_t){0})
op_404(uint64_t a, uint64_t b)
{
    return a ^ b;
}


uint64_t
emu_RTYPE__XOR(uint64_t a, uint64_t b)
{
    return (uint64_t)(op_404(a, b));
}
