// probe 350 -- binary &&
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_350(bool a, uint64_t b)
{
    return a && b;
}
