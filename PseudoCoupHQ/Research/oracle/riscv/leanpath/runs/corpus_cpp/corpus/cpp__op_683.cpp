// probe 683 -- binary <<
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_683(int32_t a, bool b)
{
    return a << b;
}
