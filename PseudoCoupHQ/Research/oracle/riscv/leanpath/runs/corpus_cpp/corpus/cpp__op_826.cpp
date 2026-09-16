// probe 826 -- binary and
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_826(int32_t a, double b)
{
    return a and b;
}
