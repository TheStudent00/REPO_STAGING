// probe 615 -- binary <=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_615(int64_t a, float b)
{
    return a <= b;
}
