// probe 932 -- binary bitand
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_932(int32_t a, uint64_t b)
{
    return a bitand b;
}
