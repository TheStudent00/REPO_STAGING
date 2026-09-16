// probe 479 -- binary ==
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_479(uint64_t a, bool b)
{
    return a == b;
}
