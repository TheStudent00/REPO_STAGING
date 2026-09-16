// probe 785 -- binary <=>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_785(bool a, bool b)
{
    return a <=> b;
}
