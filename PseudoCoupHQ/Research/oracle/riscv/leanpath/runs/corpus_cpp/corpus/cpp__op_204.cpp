// probe 204 -- binary *
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_204(bool a, int32_t b)
{
    return a * b;
}
