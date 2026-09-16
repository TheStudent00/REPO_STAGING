// probe 473 -- binary ==
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_473(int64_t a, bool b)
{
    return a == b;
}
