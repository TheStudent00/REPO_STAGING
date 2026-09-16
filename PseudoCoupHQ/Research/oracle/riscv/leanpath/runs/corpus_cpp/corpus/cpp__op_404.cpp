// probe 404 -- binary ^
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_404(uint64_t a, uint64_t b)
{
    return a ^ b;
}
