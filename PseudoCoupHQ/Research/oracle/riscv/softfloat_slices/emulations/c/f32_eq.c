#include "sfemul.h"


bool f32_eq_rm1(uint64_t v_arg, uint64_t v_arg1)
{
    const uint32_t v_i = (uint32_t)(v_arg);
    const uint32_t v_i2 = (uint32_t)(v_arg1);
    const uint32_t v_i3 = (uint32_t)(v_i & UINT32_C(0x7f800000));
    const bool v_i4 = (v_i3 != UINT32_C(0x7f800000));
    const uint32_t v_i5 = (uint32_t)(v_i & UINT32_C(0x7fffff));
    const bool v_i6 = (v_i5 == UINT32_C(0x0));
    const bool v_i7 = (v_i4 || v_i6);
    const uint32_t v_i9 = (uint32_t)(v_i2 & UINT32_C(0x7f800000));
    const bool v_i10 = (v_i9 != UINT32_C(0x7f800000));
    const uint32_t v_i11 = (uint32_t)(v_i2 & UINT32_C(0x7fffff));
    const bool v_i12 = (v_i11 == UINT32_C(0x0));
    const bool v_i13 = (v_i10 || v_i12);
    const bool v__c1 = (v_i7 && v_i13);
    const bool v_i15 = (v_i == v_i2);
    const uint32_t v_i16 = (uint32_t)(v_i2 | v_i);
    const uint32_t v_i17 = (uint32_t)(v_i16 & UINT32_C(0x7fffffff));
    const bool v_i18 = (v_i17 == UINT32_C(0x0));
    const bool v_i19 = (v_i15 || v_i18);
    const bool v__a2 = (v_i19 && v__c1);
    return v__a2;
}
