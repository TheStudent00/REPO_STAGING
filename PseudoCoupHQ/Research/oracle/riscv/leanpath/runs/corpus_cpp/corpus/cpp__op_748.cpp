// probe 748 -- binary >>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_748(bool a, double b)
{
    return a >> b;
}
