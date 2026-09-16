// probe 482 -- binary ==
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_482(float a, uint64_t b)
{
    return a == b;
}
