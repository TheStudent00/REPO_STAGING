// probe 422 -- binary ^
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_422(bool a, uint64_t b)
{
    return a ^ b;
}
