// probe 695 -- binary <<
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_695(uint64_t a, bool b)
{
    return a << b;
}
