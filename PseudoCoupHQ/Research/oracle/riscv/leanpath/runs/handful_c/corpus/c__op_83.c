/* probe 83 -- unary _Alignof */
#include <stdint.h>
#include <stdbool.h>

__typeof__(_Alignof (bool){0})
op_83(bool a)
{
    return _Alignof a;
}
