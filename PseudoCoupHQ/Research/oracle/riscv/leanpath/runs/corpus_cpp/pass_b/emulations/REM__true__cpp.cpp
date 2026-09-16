// probe 260 -- binary %
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_260(uint64_t a, uint64_t b)
{
    return a % b;
}


extern "C" uint64_t
emu_REM__true(uint64_t a, uint64_t b)
{
    return (uint64_t)(op_260(a, b));
}
