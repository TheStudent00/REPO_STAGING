// probe 620 -- binary <=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_620(uint64_t a, uint64_t b)
{
    return a <= b;
}
