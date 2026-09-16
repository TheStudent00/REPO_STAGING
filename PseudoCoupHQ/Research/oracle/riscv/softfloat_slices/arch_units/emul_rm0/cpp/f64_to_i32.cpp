#include "sfemul.hpp"

namespace sfemul {


uint32_t f64_to_i32_rm0(uint64_t v_arg)
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
    const uint32_t v_i38 = (uint32_t)(UINT32_C(0x0) - v_i37);
    const uint32_t v__m24 = (uint32_t)((v_i27) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a25 = (uint32_t)(v_i38 & v__m24);
    const uint32_t v__n26 = (uint32_t)(v__m24 ^ UINT32_C(0xffffffff));
    const uint32_t v__a27 = (uint32_t)(v_i37 & v__n26);
    const uint32_t v_i39 = (uint32_t)(v__a25 | v__a27);
    const bool v_i40 = (v_i37 == UINT32_C(0x0));
    const bool v_i41 = ((int32_t)(v_i39) > INT32_C(-1));
    const bool v_i42 = (v_i27 != v_i41);
    const bool v_i43 = (v_i40 || v_i42);
    const uint32_t v__a29 = (uint32_t)(UINT32_C(0x80000000) & v__m24);
    const uint32_t v__a31 = (uint32_t)(UINT32_C(0x7fffffff) & v__n26);
    const uint32_t v_i45 = (uint32_t)(v__a29 | v__a31);
    const bool v__n32 = (v_i43 != true);
    const bool v__c33 = (v_i30 && v__n32);
    const bool v__c38 = (v_i30 && v_i43);
    const bool v__n34 = (v_i30 != true);
    const bool v__c35 = (v__c33 || v__n34);
    const uint32_t v__m36 = (uint32_t)((v__c35) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a37 = (uint32_t)(v_i45 & v__m36);
    const uint32_t v__m39 = (uint32_t)((v__c38) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a40 = (uint32_t)(v_i39 & v__m39);
    const uint32_t v__o41 = (uint32_t)(v__a37 | v__a40);
    return v__o41;
}

}  // namespace sfemul
