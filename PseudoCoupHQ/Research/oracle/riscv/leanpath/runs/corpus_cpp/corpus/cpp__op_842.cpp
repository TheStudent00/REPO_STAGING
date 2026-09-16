// probe 842 -- binary and
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_842(float a, uint64_t b)
{
    return a and b;
}
