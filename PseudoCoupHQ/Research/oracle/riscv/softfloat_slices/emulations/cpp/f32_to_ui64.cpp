#include "sfemul.hpp"

namespace sfemul {


uint64_t f32_to_ui64_rm1(uint64_t v_arg)
{
    const uint32_t v_i = (uint32_t)(v_arg);
    const bool v_i1 = ((int32_t)(v_i) > INT32_C(-1));
    const uint32_t v_i2 = (uint32_t)((uint32_t)(v_i) >> ((UINT32_C(0x17)) & 31));
    const uint32_t v_i3 = (uint32_t)(v_i & UINT32_C(0x7fffff));
    const uint32_t v_i14 = (uint32_t)(v_i & UINT32_C(0x7f800000));
    const bool v_i15 = (v_i14 == UINT32_C(0x0));
    const uint32_t v__m1 = (uint32_t)((v_i15) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v_i4 = (uint32_t)(v_i2 & UINT32_C(0xff));
    const uint32_t v__neg = (uint32_t)(v_i2 + UINT32_C(0x2));
    const uint32_t v_i26 = (uint32_t)(v__neg & UINT32_C(0x3f));
    const uint64_t v_i27 = (uint64_t)(v_i26);
    const uint32_t v_i5 = (uint32_t)(UINT32_C(0xbe) - v_i4);
    const bool v_i6 = (v_i4 > UINT32_C(0xbe));
    const uint32_t v_i16 = (uint32_t)(v_i3 | UINT32_C(0x800000));
    const uint32_t v__a2 = (uint32_t)(v_i3 & v__m1);
    const uint32_t v__n3 = (uint32_t)(v__m1 ^ UINT32_C(0xffffffff));
    const uint32_t v__a4 = (uint32_t)(v_i16 & v__n3);
    const uint32_t v_i17 = (uint32_t)(v__a2 | v__a4);
    const bool v_i9 = (v_i3 != UINT32_C(0x0));
    const uint64_t v_i18 = (uint64_t)(v_i17);
    const uint64_t v__sh5 = (uint64_t)((uint64_t)(v_i18) << ((UINT64_C(0x28)) & 63));
    const uint64_t v_i19 = v__sh5;
    const uint64_t v__sh7 = (uint64_t)((uint64_t)(v_i19) << ((v_i27) & 63));
    const uint64_t v_i28 = v__sh7;
    const bool v_i31 = (v_i17 != UINT32_C(0x0));
    const uint64_t v_i32 = (uint64_t)((v_i31) ? 1 : 0);
    const bool v_i20 = (v_i4 == UINT32_C(0xbe));
    const bool v_i8 = (v_i4 == UINT32_C(0xff));
    const bool v_i10 = (v_i9 && v_i8);
    const bool v_i11 = (v_i10 || v_i1);
    const uint64_t v_i12 = (uint64_t)((v_i11) ? ~(uint64_t)0 : (uint64_t)0);
    const bool v_i30 = (v_i4 == UINT32_C(0x7e));
    const uint64_t v__m8 = (uint64_t)((v_i30) ? ~(uint64_t)0 : (uint64_t)0);
    const bool v_i22 = (v_i5 < UINT32_C(0x40));
    const uint64_t v_i24 = (uint64_t)(v_i5);
    const uint64_t v__sh6 = (uint64_t)((uint64_t)(v_i19) >> ((v_i24) & 63));
    const uint64_t v_i25 = v__sh6;
    const uint64_t v__a9 = (uint64_t)(v_i19 & v__m8);
    const uint64_t v__n10 = (uint64_t)(v__m8 ^ UINT64_C(0xffffffffffffffff));
    const uint64_t v__a11 = (uint64_t)(v_i32 & v__n10);
    const uint64_t v_i33 = (uint64_t)(v__a9 | v__a11);
    const uint64_t v__m12 = (uint64_t)((v_i22) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a13 = (uint64_t)(v_i28 & v__m12);
    const bool v__n14 = (v_i22 != true);
    const uint64_t v__m15 = (uint64_t)((v__n14) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a16 = (uint64_t)(v_i33 & v__m15);
    const uint64_t v__o17 = (uint64_t)(v__a13 | v__a16);
    const bool v__n18 = (v_i6 != true);
    const uint64_t v__m31 = (uint64_t)((v_i6) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a32 = (uint64_t)(v_i12 & v__m31);
    const bool v__n19 = (v_i20 != true);
    const uint64_t v__m23 = (uint64_t)((v_i20) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a24 = (uint64_t)(v_i19 & v__m23);
    const bool v__c25 = (v__n19 && v_i22);
    const bool v__c20 = (v__n18 && v__n19);
    const uint64_t v__m21 = (uint64_t)((v__c20) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a22 = (uint64_t)(v__o17 & v__m21);
    const uint64_t v__m26 = (uint64_t)((v__c25) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a27 = (uint64_t)(v_i25 & v__m26);
    const uint64_t v__o28 = (uint64_t)(v__a24 | v__a27);
    const uint64_t v__m29 = (uint64_t)((v__n18) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a30 = (uint64_t)(v__o28 & v__m29);
    const uint64_t v_i37 = (uint64_t)(v__a22 | v__a30);
    const bool v_i38 = (v_i37 != UINT64_C(0x0));
    const bool v__not = (v__a30 == UINT64_C(0x0));
    const bool v_or_cond = (v_i38 && v__not);
    const bool v__n33 = (v_i1 != true);
    const bool v__c34 = (v__n33 && v__n18);
    const bool v__c35 = (v__c34 && v_or_cond);
    const bool v__c36 = (v_i1 && v__n18);
    const bool v__c37 = (v__c35 || v__c36);
    const uint64_t v__m38 = (uint64_t)((v__c37) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a39 = (uint64_t)(v__a30 & v__m38);
    const uint64_t v__o40 = (uint64_t)(v__a32 | v__a39);
    return v__o40;
}

}  // namespace sfemul
