// probe 797 -- binary or
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_797(int64_t a, bool b)
{
    return a or b;
}
