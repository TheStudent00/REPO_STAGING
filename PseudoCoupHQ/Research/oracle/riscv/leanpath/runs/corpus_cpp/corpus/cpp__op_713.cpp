// probe 713 -- binary <<
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_713(bool a, bool b)
{
    return a << b;
}
