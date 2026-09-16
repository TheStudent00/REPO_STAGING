// probe 881 -- binary bitor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_881(float a, bool b)
{
    return a bitor b;
}
