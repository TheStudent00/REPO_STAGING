/* probe 68 -- unary _alignof */
#include <stdint.h>
#include <stdbool.h>

__typeof__(_alignof (uint64_t){0})
op_68(uint64_t a)
{
    return _alignof a;
}
