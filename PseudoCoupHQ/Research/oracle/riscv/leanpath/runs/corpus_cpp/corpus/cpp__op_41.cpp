// probe 41 -- unary *
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_41(bool a)
{
    return *a;
}
