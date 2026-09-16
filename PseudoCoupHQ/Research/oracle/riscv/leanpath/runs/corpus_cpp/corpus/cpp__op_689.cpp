// probe 689 -- binary <<
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_689(int64_t a, bool b)
{
    return a << b;
}
