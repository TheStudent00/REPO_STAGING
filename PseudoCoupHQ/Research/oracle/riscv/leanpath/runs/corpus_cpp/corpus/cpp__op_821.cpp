// probe 821 -- binary or
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_821(bool a, bool b)
{
    return a or b;
}
