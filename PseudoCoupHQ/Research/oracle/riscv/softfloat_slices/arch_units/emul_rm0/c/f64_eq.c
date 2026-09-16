#include "sfemul.h"


bool f64_eq_rm0(uint64_t v_arg, uint64_t v_arg1)
{
    const uint64_t v_i = (uint64_t)(v_arg & UINT64_C(0x7ff0000000000000));
    const bool v_i2 = (v_i != UINT64_C(0x7ff0000000000000));
    const uint64_t v_i3 = (uint64_t)(v_arg & UINT64_C(0xfffffffffffff));
    const bool v_i4 = (v_i3 == UINT64_C(0x0));
    const bool v_i5 = (v_i2 || v_i4);
    const uint64_t v_i7 = (uint64_t)(v_arg1 & UINT64_C(0x7ff0000000000000));
    const bool v_i8 = (v_i7 != UINT64_C(0x7ff0000000000000));
    const uint64_t v_i9 = (uint64_t)(v_arg1 & UINT64_C(0xfffffffffffff));
    const bool v_i10 = (v_i9 == UINT64_C(0x0));
    const bool v_i11 = (v_i8 || v_i10);
    const bool v__c1 = (v_i5 && v_i11);
    const bool v_i13 = (v_arg == v_arg1);
    const uint64_t v_i14 = (uint64_t)(v_arg1 | v_arg);
    const uint64_t v_i15 = (uint64_t)(v_i14 & UINT64_C(0x7fffffffffffffff));
    const bool v_i16 = (v_i15 == UINT64_C(0x0));
    const bool v_i17 = (v_i13 || v_i16);
    const bool v__a2 = (v_i17 && v__c1);
    return v__a2;
}
