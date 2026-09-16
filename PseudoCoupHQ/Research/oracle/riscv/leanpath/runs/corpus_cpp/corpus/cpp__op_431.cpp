// probe 431 -- binary &
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_431(int32_t a, bool b)
{
    return a & b;
}
