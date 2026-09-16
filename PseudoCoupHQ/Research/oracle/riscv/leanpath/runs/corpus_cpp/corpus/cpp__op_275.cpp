// probe 275 -- binary %
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_275(double a, bool b)
{
    return a % b;
}
