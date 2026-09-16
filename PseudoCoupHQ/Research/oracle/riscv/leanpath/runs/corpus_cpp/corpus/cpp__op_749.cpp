// probe 749 -- binary >>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_749(bool a, bool b)
{
    return a >> b;
}
