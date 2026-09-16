// probe 833 -- binary and
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_833(int64_t a, bool b)
{
    return a and b;
}
