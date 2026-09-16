/* probe 71 -- unary _alignof */
#include <stdint.h>
#include <stdbool.h>

__typeof__(_alignof (bool){0})
op_71(bool a)
{
    return _alignof a;
}
