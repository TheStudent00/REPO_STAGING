// probe 395 -- binary ^
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_395(int32_t a, bool b)
{
    return a ^ b;
}
