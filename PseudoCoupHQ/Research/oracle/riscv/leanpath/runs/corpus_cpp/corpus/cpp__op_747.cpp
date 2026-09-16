// probe 747 -- binary >>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_747(bool a, float b)
{
    return a >> b;
}
