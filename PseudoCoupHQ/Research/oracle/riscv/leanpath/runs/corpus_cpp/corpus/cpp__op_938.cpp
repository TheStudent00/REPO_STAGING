// probe 938 -- binary bitand
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_938(int64_t a, uint64_t b)
{
    return a bitand b;
}
