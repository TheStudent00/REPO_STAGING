/* probe 404 -- binary ^ */
#include <stdint.h>
#include <stdbool.h>

__typeof__((uint64_t){0} ^ (uint64_t){0})
op_404(uint64_t a, uint64_t b)
{
    return a ^ b;
}
