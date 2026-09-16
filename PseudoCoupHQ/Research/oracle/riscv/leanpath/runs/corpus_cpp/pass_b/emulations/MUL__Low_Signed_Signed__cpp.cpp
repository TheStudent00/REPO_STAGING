// probe 188 -- binary *
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_188(uint64_t a, uint64_t b)
{
    return a * b;
}


extern "C" uint64_t
emu_MUL__Low_Signed_Signed(uint64_t a, uint64_t b)
{
    return (uint64_t)(op_188(a, b));
}
