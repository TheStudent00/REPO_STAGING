// probe 875 -- binary bitor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_875(uint64_t a, bool b)
{
    return a bitor b;
}
