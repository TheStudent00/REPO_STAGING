// probe 676 -- binary <
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_676(bool a, double b)
{
    return a < b;
}
