// probe 711 -- binary <<
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_711(bool a, float b)
{
    return a << b;
}
