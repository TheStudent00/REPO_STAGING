// probe 829 -- binary and
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_829(int64_t a, int64_t b)
{
    return a and b;
}
