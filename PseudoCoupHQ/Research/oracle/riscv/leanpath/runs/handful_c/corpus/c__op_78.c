/* probe 78 -- unary _Alignof */
#include <stdint.h>
#include <stdbool.h>

__typeof__(_Alignof (int32_t){0})
op_78(int32_t a)
{
    return _Alignof a;
}
