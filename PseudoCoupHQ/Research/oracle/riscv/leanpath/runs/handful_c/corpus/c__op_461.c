/* probe 461 -- binary & */
#include <stdint.h>
#include <stdbool.h>

__typeof__((bool){0} & (bool){0})
op_461(bool a, bool b)
{
    return a & b;
}
