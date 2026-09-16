#include "sfemul.hpp"

namespace sfemul {


uint32_t f32_to_ui32_rm1(uint64_t v_arg)
{
    const uint32_t v_i = (uint32_t)(v_arg);
    const uint32_t v_i1 = (uint32_t)((uint32_t)(v_i) >> ((UINT32_C(0x17)) & 31));
    const uint32_t v_i2 = (uint32_t)(v_i & UINT32_C(0x7fffff));
    const uint32_t v_i3 = (uint32_t)(v_i1 & UINT32_C(0xff));
    const uint32_t v__neg = (uint32_t)(v_i1 + UINT32_C(0x16));
    const uint32_t v_i17 = (uint32_t)(v__neg & UINT32_C(0x3f));
    const uint64_t v_i18 = (uint64_t)(v_i17);
    const uint32_t v_i4 = (uint32_t)(v_i & UINT32_C(0x7f800000));
    const bool v_i5 = (v_i4 == UINT32_C(0x0));
    const uint32_t v__m1 = (uint32_t)((v_i5) ? ~(uint32_t)0 : (uint32_t)0);
    const bool v_i29 = ((int32_t)(v_i) < INT32_C(0));
    const uint32_t v_i6 = (uint32_t)(v_i2 | UINT32_C(0x800000));
    const uint32_t v__a2 = (uint32_t)(v_i2 & v__m1);
    const uint32_t v__n3 = (uint32_t)(v__m1 ^ UINT32_C(0xffffffff));
    const uint32_t v__a4 = (uint32_t)(v_i6 & v__n3);
    const uint32_t v_i7 = (uint32_t)(v__a2 | v__a4);
    const bool v_i27 = (v_i2 == UINT32_C(0x0));
    const uint64_t v_i8 = (uint64_t)(v_i7);
    const uint64_t v_i9 = (uint64_t)((uint64_t)(v_i8) << ((UINT64_C(0x20)) & 63));
    const uint64_t v__sh6 = (uint64_t)((uint64_t)(v_i9) << ((v_i18) & 63));
    const uint64_t v_i19 = v__sh6;
    const bool v_i20 = (v_i19 != UINT64_C(0x0));
    const uint64_t v_i21 = (uint64_t)((v_i20) ? 1 : 0);
    const bool v_i24 = (v_i7 != UINT32_C(0x0));
    const uint64_t v_i25 = (uint64_t)((v_i24) ? 1 : 0);
    const bool v_i10 = (v_i3 < UINT32_C(0xaa));
    const bool v_i12 = (v_i3 > UINT32_C(0x6b));
    const uint32_t v_i14 = (uint32_t)(UINT32_C(0xaa) - v_i3);
    const uint64_t v_i15 = (uint64_t)(v_i14);
    const uint64_t v__sh5 = (uint64_t)((uint64_t)(v_i9) >> ((v_i15) & 63));
    const uint64_t v_i16 = v__sh5;
    const uint64_t v_i22 = (uint64_t)(v_i16 | v_i21);
    const bool v_i28 = (v_i3 != UINT32_C(0xff));
    const bool v_i30 = (v_i27 || v_i28);
    const bool v_i31 = (v_i29 && v_i30);
    const bool v__n7 = (v_i10 != true);
    const uint64_t v__m8 = (uint64_t)((v__n7) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a9 = (uint64_t)(v_i9 & v__m8);
    const bool v__c10 = (v_i10 && v_i12);
    const uint64_t v__m11 = (uint64_t)((v__c10) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a12 = (uint64_t)(v_i22 & v__m11);
    const uint64_t v__o13 = (uint64_t)(v__a9 | v__a12);
    const bool v__n14 = (v_i12 != true);
    const uint64_t v__m16 = (uint64_t)((v__n14) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a17 = (uint64_t)(v_i25 & v__m16);
    const uint64_t v__o18 = (uint64_t)(v__o13 | v__a17);
    const bool v_i32 = (v__o18 == UINT64_C(0x0));
    const bool v_or_cond = (v_i31 && v_i32);
    const bool v__n20 = (v_or_cond != true);
    const bool v_i34 = (v__o18 < UINT64_C(0x100000000000));
    const uint64_t v__sh19 = (uint64_t)((uint64_t)(v__o18) >> ((UINT64_C(0xc)) & 63));
    const uint64_t v_i36 = v__sh19;
    const uint32_t v_i37 = (uint32_t)(v_i36);
    const bool v_i38 = (v__o18 > UINT64_C(0xfff));
    const bool v_i39 = (v_i31 && v_i38);
    const bool v_i41 = (v_i31 != true);
    const uint32_t v_i42 = (uint32_t)((v_i41) ? ~(uint32_t)0 : (uint32_t)0);
    const bool v__c21 = (v_i34 && v_i39);
    const bool v__n28 = (v_i39 != true);
    const bool v__c29 = (v_i34 && v__n28);
    const bool v__n23 = (v_i34 != true);
    const bool v__c25 = (v__c21 || v__n23);
    const bool v__c30 = (v__c29 && v__n20);
    const uint32_t v__m26 = (uint32_t)((v__c25) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a27 = (uint32_t)(v_i42 & v__m26);
    const uint32_t v__m31 = (uint32_t)((v__c30) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a32 = (uint32_t)(v_i37 & v__m31);
    const uint32_t v__o33 = (uint32_t)(v__a27 | v__a32);
    return v__o33;
}

}  // namespace sfemul
