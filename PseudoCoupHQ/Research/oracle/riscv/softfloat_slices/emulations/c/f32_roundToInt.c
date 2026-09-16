#include "sfemul.h"


uint64_t f32_roundToInt_rm1(uint64_t v_arg, bool v_arg1)
{
    const uint32_t v_i = (uint32_t)(v_arg);
    const uint32_t v_i2 = (uint32_t)((uint32_t)(v_i) >> ((UINT32_C(0x17)) & 31));
    const uint32_t v_i3 = (uint32_t)(v_i2 & UINT32_C(0xff));
    const bool v_i4 = (v_i3 < UINT32_C(0x7f));
    const uint32_t v_i6 = (uint32_t)(v_i & UINT32_C(0x7fffffff));
    const bool v_i7 = (v_i6 == UINT32_C(0x0));
    const uint32_t v__m1 = (uint32_t)((v_i7) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v_i8 = (uint32_t)(v_i & UINT32_C(0x80000000));
    const uint32_t v__a2 = (uint32_t)(v_i & v__m1);
    const uint32_t v__n3 = (uint32_t)(v__m1 ^ UINT32_C(0xffffffff));
    const uint32_t v__a4 = (uint32_t)(v_i8 & v__n3);
    const uint32_t v_spec_select = (uint32_t)(v__a2 | v__a4);
    const bool v_i10 = (v_i3 > UINT32_C(0x95));
    const bool v_i12 = (v_i3 != UINT32_C(0xff));
    const uint32_t v_i17 = (uint32_t)(UINT32_C(0x96) - v_i3);
    const uint32_t v__sh9 = (uint32_t)((uint32_t)(UINT32_C(0xffffffff)) << ((v_i17) & 31));
    const uint32_t v__neg = v__sh9;
    const uint32_t v_i18 = (uint32_t)(v__neg & v_i);
    const uint32_t v_i13 = (uint32_t)(v_i & UINT32_C(0x7fffff));
    const bool v_i14 = (v_i13 == UINT32_C(0x0));
    const bool v_i15 = (v_i14 || v_i12);
    const uint32_t v__m5 = (uint32_t)((v_i15) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a6 = (uint32_t)(v_i & v__m5);
    const uint32_t v__n7 = (uint32_t)(v__m5 ^ UINT32_C(0xffffffff));
    const uint32_t v__a8 = (uint32_t)(UINT32_C(0x7fc00000) & v__n7);
    const uint32_t v_spec_select4 = (uint32_t)(v__a6 | v__a8);
    const bool v__n10 = (v_i10 != true);
    const bool v__n11 = (v_i4 != true);
    const bool v__c12 = (v__n10 && v__n11);
    const uint32_t v__m13 = (uint32_t)((v__c12) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a14 = (uint32_t)(v_i18 & v__m13);
    const uint32_t v__m15 = (uint32_t)((v_i4) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a16 = (uint32_t)(v_spec_select & v__m15);
    const uint32_t v__o17 = (uint32_t)(v__a14 | v__a16);
    const uint32_t v__m19 = (uint32_t)((v_i10) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a20 = (uint32_t)(v_spec_select4 & v__m19);
    const uint32_t v__o21 = (uint32_t)(v__o17 | v__a20);
    const uint64_t v_i20 = (uint64_t)(v__o21);
    return v_i20;
}
