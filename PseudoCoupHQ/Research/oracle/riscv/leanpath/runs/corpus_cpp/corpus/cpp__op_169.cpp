// probe 169 -- binary -
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_169(bool a, int64_t b)
{
    return a - b;
}
