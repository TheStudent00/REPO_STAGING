// probe 457 -- binary &
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_457(bool a, int64_t b)
{
    return a & b;
}
