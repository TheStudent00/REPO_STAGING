#include "sfemul.h"


uint64_t f32_roundToInt_rm0(uint64_t v_arg, bool v_arg1)
{
    const uint32_t v_i = (uint32_t)(v_arg);
    const uint32_t v_i2 = (uint32_t)((uint32_t)(v_i) >> ((UINT32_C(0x17)) & 31));
    const uint32_t v_i3 = (uint32_t)(v_i2 & UINT32_C(0xff));
    const bool v_i4 = (v_i3 < UINT32_C(0x7f));
    const bool v_i16 = (v_i3 > UINT32_C(0x95));
    const uint32_t v_i6 = (uint32_t)(v_i & UINT32_C(0x7fffffff));
    const bool v_i7 = (v_i6 == UINT32_C(0x0));
    const bool v_i18 = (v_i3 != UINT32_C(0xff));
    const uint32_t v_i19 = (uint32_t)(v_i & UINT32_C(0x7fffff));
    const bool v_i20 = (v_i19 == UINT32_C(0x0));
    const bool v_i21 = (v_i20 || v_i18);
    const uint32_t v__m1 = (uint32_t)((v_i21) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a2 = (uint32_t)(v_i & v__m1);
    const uint32_t v__n3 = (uint32_t)(v__m1 ^ UINT32_C(0xffffffff));
    const uint32_t v__a4 = (uint32_t)(UINT32_C(0x7fc00000) & v__n3);
    const uint32_t v_spec_select4 = (uint32_t)(v__a2 | v__a4);
    const uint32_t v_i23 = (uint32_t)(UINT32_C(0x96) - v_i3);
    const uint32_t v__sh5 = (uint32_t)((uint32_t)(UINT32_C(0x1)) << ((v_i23) & 31));
    const uint32_t v_i24 = v__sh5;
    const bool v_i12 = (v_i3 == UINT32_C(0x7e));
    const uint32_t v_i25 = (uint32_t)(v_i24 + UINT32_C(0xffffffff));
    const uint32_t v__sh6 = (uint32_t)((uint32_t)(v_i24) >> ((UINT32_C(0x1)) & 31));
    const uint32_t v_i27 = (uint32_t)(v__sh6 + v_i);
    const uint32_t v_i28 = (uint32_t)(v_i27 & v_i25);
    const bool v_i29 = (v_i28 == UINT32_C(0x0));
    const uint32_t v__m7 = (uint32_t)((v_i29) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v_i30 = (uint32_t)(v_i24 ^ UINT32_C(0xffffffff));
    const uint32_t v__a8 = (uint32_t)(v_i30 & v__m7);
    const uint32_t v__n9 = (uint32_t)(v__m7 ^ UINT32_C(0xffffffff));
    const uint32_t v_i31 = (uint32_t)(v__a8 | v__n9);
    const uint32_t v_i32 = (uint32_t)(UINT32_C(0x0) - v_i24);
    const uint32_t v_i33 = (uint32_t)(v_i31 & v_i32);
    const uint32_t v_i34 = (uint32_t)(v_i33 & v_i27);
    const uint32_t v_i9 = (uint32_t)(v_i & UINT32_C(0x80000000));
    const bool v_i11 = (v_i19 != UINT32_C(0x0));
    const bool v_i13 = (v_i11 && v_i12);
    const uint32_t v__m11 = (uint32_t)((v_i13) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v_i14 = (uint32_t)(v_i9 | UINT32_C(0x3f800000));
    const uint32_t v__a12 = (uint32_t)(v_i14 & v__m11);
    const uint32_t v__n13 = (uint32_t)(v__m11 ^ UINT32_C(0xffffffff));
    const uint32_t v__a14 = (uint32_t)(v_i9 & v__n13);
    const uint32_t v_spec_select = (uint32_t)(v__a12 | v__a14);
    const bool v__c15 = (v_i7 && v_i4);
    const uint32_t v__m16 = (uint32_t)((v__c15) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a17 = (uint32_t)(v_i & v__m16);
    const bool v__n18 = (v_i7 != true);
    const bool v__c19 = (v__n18 && v_i4);
    const uint32_t v__m20 = (uint32_t)((v__c19) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a21 = (uint32_t)(v_spec_select & v__m20);
    const uint32_t v__o22 = (uint32_t)(v__a17 | v__a21);
    const bool v__n24 = (v_i4 != true);
    const bool v__n23 = (v_i16 != true);
    const bool v__c25 = (v__n23 && v__n24);
    const uint32_t v__m26 = (uint32_t)((v__c25) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a27 = (uint32_t)(v_i34 & v__m26);
    const uint32_t v__o28 = (uint32_t)(v__o22 | v__a27);
    const uint32_t v__m30 = (uint32_t)((v_i16) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a31 = (uint32_t)(v_spec_select4 & v__m30);
    const uint32_t v__o32 = (uint32_t)(v__o28 | v__a31);
    const uint64_t v_i36 = (uint64_t)(v__o32);
    return v_i36;
}
