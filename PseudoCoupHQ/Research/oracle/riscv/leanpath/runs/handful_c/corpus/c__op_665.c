/* probe 665 -- binary < */
#include <stdint.h>
#include <stdbool.h>

__typeof__((float){0} < (bool){0})
op_665(float a, bool b)
{
    return a < b;
}
