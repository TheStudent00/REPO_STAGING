// probe 223 -- binary /
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_223(uint64_t a, int64_t b)
{
    return a / b;
}
