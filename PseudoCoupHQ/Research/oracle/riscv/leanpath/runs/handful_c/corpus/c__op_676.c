/* probe 676 -- binary < */
#include <stdint.h>
#include <stdbool.h>

__typeof__((bool){0} < (double){0})
op_676(bool a, double b)
{
    return a < b;
}
