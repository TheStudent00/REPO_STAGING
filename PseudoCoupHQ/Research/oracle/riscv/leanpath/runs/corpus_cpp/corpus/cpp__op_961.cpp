// probe 961 -- binary bitand
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_961(bool a, int64_t b)
{
    return a bitand b;
}
