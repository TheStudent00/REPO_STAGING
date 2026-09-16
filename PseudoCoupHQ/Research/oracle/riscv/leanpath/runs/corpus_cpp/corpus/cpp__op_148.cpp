// probe 148 -- binary -
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_148(int64_t a, double b)
{
    return a - b;
}
