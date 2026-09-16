// probe 681 -- binary <<
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_681(int32_t a, float b)
{
    return a << b;
}
