// probe 246 -- binary %
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_246(int32_t a, int32_t b)
{
    return a % b;
}


extern "C" uint64_t
emu_REMW__false(uint64_t a, uint64_t b)
{
    return (uint64_t)(op_246(a, b));
}
