// probe 599 -- binary >=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_599(double a, bool b)
{
    return a >= b;
}
