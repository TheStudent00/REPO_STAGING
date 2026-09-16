/* probe 67 -- unary _alignof */
#include <stdint.h>
#include <stdbool.h>

__typeof__(_alignof (int64_t){0})
op_67(int64_t a)
{
    return _alignof a;
}
