// probe 206 -- binary *
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_206(bool a, uint64_t b)
{
    return a * b;
}
