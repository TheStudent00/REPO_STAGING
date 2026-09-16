// probe 728 -- binary >>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_728(uint64_t a, uint64_t b)
{
    return a >> b;
}


extern "C" uint64_t
emu_SHIFTIOP__SRLI(uint64_t a, uint64_t shamt)
{
    return (uint64_t)(op_728(a, shamt));
}
