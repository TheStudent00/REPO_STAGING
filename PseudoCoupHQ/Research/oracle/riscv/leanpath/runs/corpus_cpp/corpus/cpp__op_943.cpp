// probe 943 -- binary bitand
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_943(uint64_t a, int64_t b)
{
    return a bitand b;
}
