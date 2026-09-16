/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of ZBB_RTYPE__op_MIN__rd__c__native_first.  The term's text, LITERAL:
    */
#include <stdint.h>

uint64_t
emu_ZBB_RTYPE__op_MIN__rd__c__native_first(uint64_t a, uint64_t b)
{
    int v0 = (((int64_t)((uint64_t)b) <= (int64_t)((uint64_t)a))) ? 1 : 0;
    uint64_t v1 = ((v0) ? (uint64_t)((uint64_t)b) : (uint64_t)((uint64_t)a));
    return (uint64_t)(v1);
}
