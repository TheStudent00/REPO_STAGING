// probe 502 -- binary !=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_502(int32_t a, double b)
{
    return a != b;
}
