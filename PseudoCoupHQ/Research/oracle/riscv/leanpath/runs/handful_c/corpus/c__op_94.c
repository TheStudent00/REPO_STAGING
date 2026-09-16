/* probe 94 -- unary ++ */
#include <stdint.h>
#include <stdbool.h>

__typeof__((double){0}++)
op_94(double a)
{
    return a++;
}
