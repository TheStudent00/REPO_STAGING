// probe 601 -- binary >=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_601(bool a, int64_t b)
{
    return a >= b;
}
