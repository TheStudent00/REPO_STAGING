// probe 400 -- binary ^
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_400(int64_t a, double b)
{
    return a ^ b;
}
