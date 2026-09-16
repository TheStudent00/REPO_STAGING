// probe 314 -- binary ||
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_314(bool a, uint64_t b)
{
    return a || b;
}
