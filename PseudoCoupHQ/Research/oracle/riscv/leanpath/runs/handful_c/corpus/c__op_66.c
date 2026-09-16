/* probe 66 -- unary _alignof */
#include <stdint.h>
#include <stdbool.h>

__typeof__(_alignof (int32_t){0})
op_66(int32_t a)
{
    return _alignof a;
}
