// probe 528 -- binary !=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_528(bool a, int32_t b)
{
    return a != b;
}
