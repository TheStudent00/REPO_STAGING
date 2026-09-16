#include "sfemul.hpp"

namespace sfemul {


uint32_t f64_to_ui32_rm0(uint64_t v_arg)
{
    const uint64_t v_i = (uint64_t)((uint64_t)(v_arg) >> ((UINT64_C(0x34)) & 63));
    const uint16_t v_i1 = (uint16_t)(v_i);
    const uint16_t v_i2 = (uint16_t)(v_i1 & UINT32_C(0x7ff));
    const uint64_t v__neg = (uint64_t)(v_i + UINT64_C(0x19));
    const uint64_t v_i14 = (uint64_t)(v__neg & UINT64_C(0x3f));
    const uint64_t v_i3 = (uint64_t)(v_arg & UINT64_C(0xfffffffffffff));
    const bool v_i4 = (v_i2 == UINT32_C(0x0));
    const uint64_t v__m1 = (uint64_t)((v_i4) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v_i5 = (uint64_t)(v_i3 | UINT64_C(0x10000000000000));
    const uint64_t v__a2 = (uint64_t)(v_i3 & v__m1);
    const uint64_t v__n3 = (uint64_t)(v__m1 ^ UINT64_C(0xffffffffffffffff));
    const uint64_t v__a4 = (uint64_t)(v_i5 & v__n3);
    const uint64_t v_i6 = (uint64_t)(v__a2 | v__a4);
    const uint64_t v__sh6 = (uint64_t)((uint64_t)(v_i6) << ((v_i14) & 63));
    const uint64_t v_i15 = v__sh6;
    const bool v_i16 = (v_i15 != UINT64_C(0x0));
    const uint64_t v_i17 = (uint64_t)((v_i16) ? 1 : 0);
    const bool v_i23 = (v_i3 == UINT64_C(0x0));
    const bool v_i7 = (v_i2 < UINT32_C(0x427));
    const bool v_i9 = (v_i2 > UINT32_C(0x3e8));
    const uint16_t v_i11 = (uint16_t)(UINT32_C(0x427) - v_i2);
    const uint64_t v_i12 = (uint64_t)(v_i11);
    const uint64_t v__sh5 = (uint64_t)((uint64_t)(v_i6) >> ((v_i12) & 63));
    const uint64_t v_i13 = v__sh5;
    const uint64_t v_i18 = (uint64_t)(v_i13 | v_i17);
    const bool v_i24 = (v_i2 != UINT32_C(0x7ff));
    const bool v_i26 = (v_i23 || v_i24);
    const bool v_i20 = (v_i6 != UINT64_C(0x0));
    const uint64_t v_i21 = (uint64_t)((v_i20) ? 1 : 0);
    const bool v__n7 = (v_i7 != true);
    const uint64_t v__m8 = (uint64_t)((v__n7) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a9 = (uint64_t)(v_i6 & v__m8);
    const bool v__c10 = (v_i9 && v_i7);
    const uint64_t v__m11 = (uint64_t)((v__c10) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a12 = (uint64_t)(v_i18 & v__m11);
    const uint64_t v__o13 = (uint64_t)(v__a9 | v__a12);
    const bool v__n14 = (v_i9 != true);
    const uint64_t v__m16 = (uint64_t)((v__n14) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a17 = (uint64_t)(v_i21 & v__m16);
    const uint64_t v__o18 = (uint64_t)(v__o13 | v__a17);
    const bool v_i25 = ((int64_t)(v_arg) < INT64_C(0));
    const bool v_i27 = (v_i25 && v_i26);
    const uint16_t v_i28 = (uint16_t)(v__o18);
    const uint16_t v_i29 = (uint16_t)(v_i28 & UINT32_C(0xfff));
    const bool v_i35 = (v_i29 == UINT32_C(0x800));
    const uint32_t v__m20 = (uint32_t)((v_i35) ? ~(uint32_t)0 : (uint32_t)0);
    const bool v_i30 = (v__o18 < UINT64_C(0xffffffff800));
    const uint64_t v_i32 = (uint64_t)(v__o18 + UINT64_C(0x800));
    const uint64_t v__sh19 = (uint64_t)((uint64_t)(v_i32) >> ((UINT64_C(0xc)) & 63));
    const uint64_t v_i33 = v__sh19;
    const uint32_t v_i34 = (uint32_t)(v_i33);
    const uint32_t v_i36 = (uint32_t)(v_i34 & UINT32_C(0xfffffffe));
    const uint32_t v__a21 = (uint32_t)(v_i36 & v__m20);
    const uint32_t v__n22 = (uint32_t)(v__m20 ^ UINT32_C(0xffffffff));
    const uint32_t v__a23 = (uint32_t)(v_i34 & v__n22);
    const uint32_t v_i37 = (uint32_t)(v__a21 | v__a23);
    const bool v_i38 = (v_i37 != UINT32_C(0x0));
    const bool v_i39 = (v_i27 && v_i38);
    const bool v_i41 = (v_i27 != true);
    const uint32_t v_i42 = (uint32_t)((v_i41) ? ~(uint32_t)0 : (uint32_t)0);
    const bool v__c24 = (v_i30 && v_i39);
    const bool v__n29 = (v_i39 != true);
    const bool v__c30 = (v_i30 && v__n29);
    const bool v__n25 = (v_i30 != true);
    const bool v__c26 = (v__c24 || v__n25);
    const uint32_t v__m27 = (uint32_t)((v__c26) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a28 = (uint32_t)(v_i42 & v__m27);
    const uint32_t v__m31 = (uint32_t)((v__c30) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a32 = (uint32_t)(v_i37 & v__m31);
    const uint32_t v__o33 = (uint32_t)(v__a28 | v__a32);
    return v__o33;
}

}  // namespace sfemul
