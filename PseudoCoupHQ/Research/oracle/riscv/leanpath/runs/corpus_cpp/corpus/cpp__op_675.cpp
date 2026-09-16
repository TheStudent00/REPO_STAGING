// probe 675 -- binary <
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_675(bool a, float b)
{
    return a < b;
}
