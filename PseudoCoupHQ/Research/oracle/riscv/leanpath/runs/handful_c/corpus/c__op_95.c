/* probe 95 -- unary ++ */
#include <stdint.h>
#include <stdbool.h>

__typeof__((bool){0}++)
op_95(bool a)
{
    return a++;
}
