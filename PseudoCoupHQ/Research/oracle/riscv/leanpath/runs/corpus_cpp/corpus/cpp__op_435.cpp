// probe 435 -- binary &
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_435(int64_t a, float b)
{
    return a & b;
}
