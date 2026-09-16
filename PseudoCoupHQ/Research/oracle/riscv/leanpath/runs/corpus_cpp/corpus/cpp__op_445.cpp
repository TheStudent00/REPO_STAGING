// probe 445 -- binary &
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_445(float a, int64_t b)
{
    return a & b;
}
