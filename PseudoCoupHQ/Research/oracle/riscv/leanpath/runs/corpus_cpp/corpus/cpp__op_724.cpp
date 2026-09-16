// probe 724 -- binary >>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_724(int64_t a, double b)
{
    return a >> b;
}
