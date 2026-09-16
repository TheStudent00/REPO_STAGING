// probe 313 -- binary ||
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_313(bool a, int64_t b)
{
    return a || b;
}
