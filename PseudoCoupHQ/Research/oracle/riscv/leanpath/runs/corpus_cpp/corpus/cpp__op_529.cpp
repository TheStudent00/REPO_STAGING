// probe 529 -- binary !=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_529(bool a, int64_t b)
{
    return a != b;
}
