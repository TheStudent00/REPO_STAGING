// probe 281 -- binary %
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_281(bool a, bool b)
{
    return a % b;
}
