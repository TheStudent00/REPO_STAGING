#include "sfemul.hpp"

namespace sfemul {


uint64_t i64_to_f64_rm0(uint64_t v_arg)
{
    const uint64_t v_i = (uint64_t)(v_arg & UINT64_C(0x7fffffffffffffff));
    const bool v_i1 = (v_i == UINT64_C(0x0));
    const bool v_i3 = ((int64_t)(v_arg) < INT64_C(0));
    const uint64_t v__m1 = (uint64_t)((v_i3) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v_i4 = (uint64_t)(UINT64_C(0xc3e0000000000000) & v__m1);
    const uint64_t v__k2 = sf_abs64(v_arg);
    const bool v_i7 = (v_arg == UINT64_C(0x0));
    const uint64_t v__k3 = sf_ctlz64(v__k2);
    const uint64_t v_i9 = v__k3;
    const uint8_t v_i10 = (uint8_t)(v_i9);
    const uint8_t v_i11 = (uint8_t)(v_i10 + UINT32_C(0xff));
    const bool v__n4 = (v_i7 != true);
    const uint8_t v__m5 = (uint8_t)((v__n4) ? ~(uint8_t)0 : (uint8_t)0);
    const uint8_t v__a6 = (uint8_t)(v_i11 & v__m5);
    const uint8_t v__m7 = (uint8_t)((v_i7) ? ~(uint8_t)0 : (uint8_t)0);
    const uint8_t v__a8 = (uint8_t)(UINT32_C(0x3f) & v__m7);
    const uint8_t v__o9 = (uint8_t)(v__a6 | v__a8);
    const uint64_t v__m14 = (uint64_t)((v_i7) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__n15 = (uint64_t)(v__m14 ^ UINT64_C(0xffffffffffffffff));
    const bool v__n10 = (v_i1 != true);
    const uint64_t v__m22 = (uint64_t)((v_i1) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a23 = (uint64_t)(v_i4 & v__m22);
    const uint8_t v__m11 = (uint8_t)((v__n10) ? ~(uint8_t)0 : (uint8_t)0);
    const uint8_t v__a12 = (uint8_t)(v__o9 & v__m11);
    const uint32_t v_i14 = (uint32_t)(int32_t)(int8_t)(v__a12);
    const uint16_t v_i15 = (uint16_t)(int16_t)(int8_t)(v__a12);
    const uint16_t v_i16 = (uint16_t)(UINT32_C(0x43c) - v_i15);
    const bool v_i17 = ((int8_t)(v__a12) > INT32_C(9));
    const uint64_t v_i19 = (uint64_t)(v_i16);
    const uint64_t v__sh13 = (uint64_t)((uint64_t)(v_i19) << ((UINT64_C(0x34)) & 63));
    const uint64_t v_i21 = v__sh13;
    const uint64_t v_i22 = (uint64_t)(v_i21 & v__n15);
    const uint64_t v_i20 = (uint64_t)(v_arg & UINT64_C(0x8000000000000000));
    const uint32_t v_i23 = (uint32_t)(v_i14 + UINT32_C(0xfffffff6));
    const uint64_t v_i24 = (uint64_t)(v_i23);
    const uint64_t v__sh16 = (uint64_t)((uint64_t)(v__k2) << ((v_i24) & 63));
    const uint64_t v_i25 = v__sh16;
    const uint64_t v_i26 = (uint64_t)(v_i25 + v_i20);
    const uint64_t v_i27 = (uint64_t)(v_i26 + v_i22);
    const uint64_t v_i28 = (uint64_t)(v_i14);
    const uint64_t v__sh17 = (uint64_t)((uint64_t)(v__k2) << ((v_i28) & 63));
    const uint64_t v_i29 = v__sh17;
    const uint16_t v_i30 = (uint16_t)(v_i29);
    const uint16_t v_i31 = (uint16_t)(v_i30 & UINT32_C(0x3ff));
    const uint64_t v_i32 = (uint64_t)(v_i29 + UINT64_C(0x200));
    const uint64_t v__sh18 = (uint64_t)((uint64_t)(v_i32) >> ((UINT64_C(0xa)) & 63));
    const bool v_i35 = (v_i31 == UINT32_C(0x200));
    const uint64_t v_i36 = (uint64_t)((v_i35) ? 1 : 0);
    const uint64_t v_i37 = (uint64_t)(v_i36 ^ UINT64_C(0xffffffffffffffff));
    const uint64_t v_i38 = (uint64_t)(v__sh18 & v_i37);
    const bool v_i39 = (v_i38 == UINT64_C(0x0));
    const uint64_t v__m20 = (uint64_t)((v_i39) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__n21 = (uint64_t)(v__m20 ^ UINT64_C(0xffffffffffffffff));
    const uint64_t v_i43 = (uint64_t)(v_i21 & v__n21);
    const uint64_t v_i44 = (uint64_t)(v_i38 | v_i20);
    const uint64_t v_i45 = (uint64_t)(v_i44 + v_i43);
    const bool v__c24 = (v__n10 && v_i17);
    const uint64_t v__m25 = (uint64_t)((v__c24) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a26 = (uint64_t)(v_i27 & v__m25);
    const uint64_t v__o27 = (uint64_t)(v__a23 | v__a26);
    const bool v__n28 = (v_i17 != true);
    const bool v__c29 = (v__n10 && v__n28);
    const uint64_t v__m30 = (uint64_t)((v__c29) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a31 = (uint64_t)(v_i45 & v__m30);
    const uint64_t v__o32 = (uint64_t)(v__o27 | v__a31);
    return v__o32;
}

}  // namespace sfemul
