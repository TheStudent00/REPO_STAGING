// probe 866 -- binary bitor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_866(int64_t a, uint64_t b)
{
    return a bitor b;
}
