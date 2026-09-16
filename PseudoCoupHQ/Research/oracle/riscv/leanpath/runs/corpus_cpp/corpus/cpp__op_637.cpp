// probe 637 -- binary <=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_637(bool a, int64_t b)
{
    return a <= b;
}
