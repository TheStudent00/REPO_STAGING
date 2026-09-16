// probe 471 -- binary ==
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_471(int64_t a, float b)
{
    return a == b;
}
