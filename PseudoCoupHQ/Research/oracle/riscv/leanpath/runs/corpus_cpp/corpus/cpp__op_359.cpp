// probe 359 -- binary |
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_359(int32_t a, bool b)
{
    return a | b;
}
