// probe 783 -- binary <=>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_783(bool a, float b)
{
    return a <=> b;
}
