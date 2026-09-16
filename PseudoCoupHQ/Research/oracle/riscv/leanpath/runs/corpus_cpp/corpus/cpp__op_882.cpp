// probe 882 -- binary bitor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_882(double a, int32_t b)
{
    return a bitor b;
}
