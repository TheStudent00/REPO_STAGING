// probe 995 -- binary not_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_995(double a, bool b)
{
    return a not_eq b;
}
