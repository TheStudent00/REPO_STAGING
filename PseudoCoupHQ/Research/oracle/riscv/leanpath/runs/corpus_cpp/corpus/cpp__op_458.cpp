// probe 458 -- binary &
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_458(bool a, uint64_t b)
{
    return a & b;
}
