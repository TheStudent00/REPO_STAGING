// probe 839 -- binary and
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_839(uint64_t a, bool b)
{
    return a and b;
}
