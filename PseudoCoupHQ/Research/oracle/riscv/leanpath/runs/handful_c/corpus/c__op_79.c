/* probe 79 -- unary _Alignof */
#include <stdint.h>
#include <stdbool.h>

__typeof__(_Alignof (int64_t){0})
op_79(int64_t a)
{
    return _Alignof a;
}
