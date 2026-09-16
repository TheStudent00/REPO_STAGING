// probe 861 -- binary bitor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_861(int32_t a, float b)
{
    return a bitor b;
}
