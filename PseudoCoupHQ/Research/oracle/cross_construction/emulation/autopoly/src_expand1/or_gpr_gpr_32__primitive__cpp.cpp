// probe 317 -- binary ||
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
emu_or_gpr_gpr_32__primitive__cpp(bool a, bool b)
{
    return a || b;
}
