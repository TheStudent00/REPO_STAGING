// probe 107 -- binary +
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_107(int32_t a, bool b)
{
    return a + b;
}
