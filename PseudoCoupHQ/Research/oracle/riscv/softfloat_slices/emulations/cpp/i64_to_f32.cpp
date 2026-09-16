#include "sfemul.hpp"

namespace sfemul {


uint64_t i64_to_f32_rm1(uint64_t v_arg)
{
    const bool v_i = ((int64_t)(v_arg) < INT64_C(0));
    const uint32_t v__m20 = (uint32_t)((v_i) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v_i43 = (uint32_t)(UINT32_C(0x80000000) & v__m20);
    const uint64_t v_i1 = sf_abs64(v_arg);
    const bool v_i2 = (v_arg == UINT64_C(0x0));
    const bool v__n15 = (v_i2 != true);
    const uint64_t v__k1 = sf_ctlz64(v_i1);
    const uint64_t v_i4 = v__k1;
    const uint8_t v_i5 = (uint8_t)(v_i4);
    const uint64_t v_i23 = (uint64_t)(UINT64_C(0x21) - v_i4);
    const uint64_t v_i24 = (uint64_t)(v_i23 & UINT64_C(0xff));
    const bool v_i6 = (v_i1 < UINT64_C(0x1000000));
    const uint8_t v_i20 = (uint8_t)(v_i5 + UINT32_C(0xdf));
    const uint8_t v_i8 = (uint8_t)(v_i5 + UINT32_C(0xd8));
    const uint32_t v_i9 = (uint32_t)(v_i8);
    const bool v_i21 = (v_i1 > UINT64_C(0x7fffffff));
    const uint64_t v__sh2 = (uint64_t)((uint64_t)(v_arg) >> ((UINT64_C(0x20)) & 63));
    const uint32_t v_i11 = (uint32_t)(v__sh2);
    const uint32_t v_i12 = (uint32_t)(v_i11 & UINT32_C(0x80000000));
    const uint32_t v_i15 = (uint32_t)(v_i12 | UINT32_C(0x4a800000));
    const uint32_t v_i13 = (uint32_t)(v_i1);
    const uint32_t v__sh3 = (uint32_t)((uint32_t)(v_i13) << ((v_i9) & 31));
    const uint32_t v_i14 = v__sh3;
    const uint32_t v__sh4 = (uint32_t)((uint32_t)(v_i9) << ((UINT32_C(0x17)) & 31));
    const uint32_t v_i17 = (uint32_t)(v_i15 - v__sh4);
    const uint32_t v_i18 = (uint32_t)(v_i17 + v_i14);
    const uint64_t v__sh5 = (uint64_t)((uint64_t)(v_i1) >> ((v_i24) & 63));
    const uint64_t v_i25 = v__sh5;
    const uint64_t v__sh6 = (uint64_t)((uint64_t)(UINT64_C(0xffffffffffffffff)) << ((v_i24) & 63));
    const uint64_t v_i26 = v__sh6;
    const uint64_t v_i27 = (uint64_t)(v_i26 ^ UINT64_C(0xffffffffffffffff));
    const uint64_t v_i28 = (uint64_t)(v_i1 & v_i27);
    const bool v_i29 = (v_i28 != UINT64_C(0x0));
    const uint64_t v_i30 = (uint64_t)((v_i29) ? 1 : 0);
    const uint64_t v_i31 = (uint64_t)(v_i25 | v_i30);
    const uint32_t v_i32 = (uint32_t)(v_i31);
    const uint32_t v_i35 = (uint32_t)(v_i20);
    const uint32_t v__sh7 = (uint32_t)((uint32_t)(v_i13) << ((v_i35) & 31));
    const uint32_t v_i36 = v__sh7;
    const uint32_t v_i38 = (uint32_t)(int32_t)(int8_t)(v_i20);
    const uint32_t v__sh21 = (uint32_t)((uint32_t)(v_i38) << ((UINT32_C(0x17)) & 31));
    const uint32_t v_i45 = (uint32_t)(UINT32_C(0x4e000000) - v__sh21);
    const uint32_t v__m8 = (uint32_t)((v_i21) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a9 = (uint32_t)(v_i32 & v__m8);
    const bool v__n10 = (v_i21 != true);
    const uint32_t v__m11 = (uint32_t)((v__n10) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a12 = (uint32_t)(v_i36 & v__m11);
    const uint32_t v__o13 = (uint32_t)(v__a9 | v__a12);
    const bool v__n14 = (v_i6 != true);
    const uint32_t v__m26 = (uint32_t)((v_i6) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a27 = (uint32_t)(v_i18 & v__m26);
    const bool v__c16 = (v__n14 && v__n15);
    const uint32_t v__m17 = (uint32_t)((v__c16) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a18 = (uint32_t)(v__o13 & v__m17);
    const uint32_t v__m24 = (uint32_t)((v__n14) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__m29 = (uint32_t)((v__n15) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__sh19 = (uint32_t)((uint32_t)(v__a18) >> ((UINT32_C(0x7)) & 31));
    const uint32_t v_i39 = v__sh19;
    const uint32_t v_i47 = (uint32_t)(v_i39 | v_i43);
    const bool v_i42 = (v__a18 < UINT32_C(0x80));
    const uint32_t v__m22 = (uint32_t)((v_i42) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__n23 = (uint32_t)(v__m22 ^ UINT32_C(0xffffffff));
    const uint32_t v_i46 = (uint32_t)(v_i45 & v__n23);
    const uint32_t v_i48 = (uint32_t)(v_i47 + v_i46);
    const uint32_t v__a25 = (uint32_t)(v_i48 & v__m24);
    const uint32_t v__o28 = (uint32_t)(v__a25 | v__a27);
    const uint32_t v__a30 = (uint32_t)(v__o28 & v__m29);
    const uint64_t v_i50 = (uint64_t)(v__a30);
    return v_i50;
}

}  // namespace sfemul
