// probe 965 -- binary bitand
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_965(bool a, bool b)
{
    return a bitand b;
}
