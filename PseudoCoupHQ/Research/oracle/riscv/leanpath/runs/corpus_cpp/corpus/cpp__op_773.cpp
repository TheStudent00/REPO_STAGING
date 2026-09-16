// probe 773 -- binary <=>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_773(float a, bool b)
{
    return a <=> b;
}
