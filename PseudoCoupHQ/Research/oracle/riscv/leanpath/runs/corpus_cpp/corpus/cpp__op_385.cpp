// probe 385 -- binary |
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_385(bool a, int64_t b)
{
    return a | b;
}
