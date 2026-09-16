// probe 869 -- binary bitor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_869(int64_t a, bool b)
{
    return a bitor b;
}
