// probe 830 -- binary and
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_830(int64_t a, uint64_t b)
{
    return a and b;
}
