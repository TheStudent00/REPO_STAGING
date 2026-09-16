// probe 827 -- binary and
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_827(int32_t a, bool b)
{
    return a and b;
}
