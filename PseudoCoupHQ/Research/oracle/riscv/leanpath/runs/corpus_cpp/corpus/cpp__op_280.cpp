// probe 280 -- binary %
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_280(bool a, double b)
{
    return a % b;
}
