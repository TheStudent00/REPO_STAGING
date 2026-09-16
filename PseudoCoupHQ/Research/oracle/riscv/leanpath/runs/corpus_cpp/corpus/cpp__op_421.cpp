// probe 421 -- binary ^
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_421(bool a, int64_t b)
{
    return a ^ b;
}
