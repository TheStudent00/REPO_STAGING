// probe 102 -- binary +
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
emu_lea_lea_mem_32__primitive__cpp(int32_t a, int32_t b)
{
    return a + b;
}
