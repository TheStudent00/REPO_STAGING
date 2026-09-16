// probe 718 -- binary >>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_718(int32_t a, double b)
{
    return a >> b;
}
