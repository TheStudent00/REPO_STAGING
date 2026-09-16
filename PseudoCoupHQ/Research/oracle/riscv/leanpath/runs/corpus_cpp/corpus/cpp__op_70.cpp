// probe 70 -- unary co_await
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_70(double a)
{
    return co_await a;
}
