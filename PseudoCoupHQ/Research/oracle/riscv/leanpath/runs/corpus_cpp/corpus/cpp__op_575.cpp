// probe 575 -- binary >=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_575(int32_t a, bool b)
{
    return a >= b;
}
