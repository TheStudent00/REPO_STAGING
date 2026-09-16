// probe 507 -- binary !=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_507(int64_t a, float b)
{
    return a != b;
}
