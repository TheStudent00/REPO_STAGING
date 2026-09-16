// probe 170 -- binary -
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_170(bool a, uint64_t b)
{
    return a - b;
}
