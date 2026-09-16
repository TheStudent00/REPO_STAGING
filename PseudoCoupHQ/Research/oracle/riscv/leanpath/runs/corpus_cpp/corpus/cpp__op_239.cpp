// probe 239 -- binary /
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_239(double a, bool b)
{
    return a / b;
}
