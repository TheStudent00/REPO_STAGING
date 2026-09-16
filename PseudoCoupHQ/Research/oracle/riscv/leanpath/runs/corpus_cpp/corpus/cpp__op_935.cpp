// probe 935 -- binary bitand
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_935(int32_t a, bool b)
{
    return a bitand b;
}
