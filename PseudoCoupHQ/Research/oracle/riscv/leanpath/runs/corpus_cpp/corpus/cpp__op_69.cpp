// probe 69 -- unary co_await
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_69(float a)
{
    return co_await a;
}
