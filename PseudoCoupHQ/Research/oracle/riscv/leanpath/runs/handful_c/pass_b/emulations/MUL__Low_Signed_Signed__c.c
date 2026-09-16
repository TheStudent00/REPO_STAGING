/* probe 188 -- binary * */
#include <stdint.h>
#include <stdbool.h>

__typeof__((uint64_t){0} * (uint64_t){0})
op_188(uint64_t a, uint64_t b)
{
    return a * b;
}


uint64_t
emu_MUL__Low_Signed_Signed(uint64_t a, uint64_t b)
{
    return (uint64_t)(op_188(a, b));
}
