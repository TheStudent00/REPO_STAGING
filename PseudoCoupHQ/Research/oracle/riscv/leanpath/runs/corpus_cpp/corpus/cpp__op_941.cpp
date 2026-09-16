// probe 941 -- binary bitand
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_941(int64_t a, bool b)
{
    return a bitand b;
}
