/* probe 65 -- unary __alignof */
#include <stdint.h>
#include <stdbool.h>

__typeof__(__alignof (bool){0})
op_65(bool a)
{
    return __alignof a;
}
