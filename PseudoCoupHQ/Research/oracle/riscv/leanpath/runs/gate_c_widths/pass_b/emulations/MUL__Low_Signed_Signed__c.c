/* probe 181 -- binary * */
#include <stdint.h>
#include <stdbool.h>

__typeof__((int64_t){0} * (int64_t){0})
op_181(int64_t a, int64_t b)
{
    return a * b;
}


uint64_t
emu_MUL__Low_Signed_Signed(uint64_t a, uint64_t b)
{
    return (uint64_t)(op_181(a, b));
}
