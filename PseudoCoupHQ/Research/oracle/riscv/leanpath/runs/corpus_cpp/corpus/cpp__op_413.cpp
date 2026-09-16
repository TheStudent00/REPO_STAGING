// probe 413 -- binary ^
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_413(float a, bool b)
{
    return a ^ b;
}
