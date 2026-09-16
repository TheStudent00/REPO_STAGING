// probe 133 -- binary +
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_133(bool a, int64_t b)
{
    return a + b;
}
