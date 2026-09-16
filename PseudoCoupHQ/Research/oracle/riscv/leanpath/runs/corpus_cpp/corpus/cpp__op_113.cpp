// probe 113 -- binary +
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_113(int64_t a, bool b)
{
    return a + b;
}
