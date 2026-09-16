// probe 269 -- binary %
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_269(float a, bool b)
{
    return a % b;
}
