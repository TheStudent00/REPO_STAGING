// probe 953 -- binary bitand
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_953(float a, bool b)
{
    return a bitand b;
}
