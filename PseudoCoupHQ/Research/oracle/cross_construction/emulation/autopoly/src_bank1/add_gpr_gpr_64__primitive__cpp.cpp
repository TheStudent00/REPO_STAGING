// probe 133 -- binary +
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
emu_add_gpr_gpr_64__primitive__cpp(bool a, int64_t b)
{
    return a + b;
}
