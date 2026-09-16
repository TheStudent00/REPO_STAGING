// probe 677 -- binary <
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_677(bool a, bool b)
{
    return a < b;
}
