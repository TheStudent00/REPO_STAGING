/* probe 279 -- binary % */
#include <stdint.h>
#include <stdbool.h>

__typeof__((bool){0} % (float){0})
op_279(bool a, float b)
{
    return a % b;
}
