// probe 409 -- binary ^
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_409(float a, int64_t b)
{
    return a ^ b;
}
