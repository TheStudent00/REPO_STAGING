// probe 759 -- binary <=>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_759(int64_t a, float b)
{
    return a <=> b;
}
