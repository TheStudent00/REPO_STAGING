// probe 493 -- binary ==
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_493(bool a, int64_t b)
{
    return a == b;
}
