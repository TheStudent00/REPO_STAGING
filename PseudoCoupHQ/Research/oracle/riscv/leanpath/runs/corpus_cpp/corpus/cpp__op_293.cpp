// probe 293 -- binary ||
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_293(int64_t a, bool b)
{
    return a || b;
}
