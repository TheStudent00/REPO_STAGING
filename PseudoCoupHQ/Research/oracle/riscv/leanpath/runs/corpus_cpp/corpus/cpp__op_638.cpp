// probe 638 -- binary <=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_638(bool a, uint64_t b)
{
    return a <= b;
}
