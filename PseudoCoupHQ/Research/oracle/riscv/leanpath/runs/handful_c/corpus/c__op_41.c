/* probe 41 -- unary ++ */
#include <stdint.h>
#include <stdbool.h>

__typeof__(++(bool){0})
op_41(bool a)
{
    return ++a;
}
