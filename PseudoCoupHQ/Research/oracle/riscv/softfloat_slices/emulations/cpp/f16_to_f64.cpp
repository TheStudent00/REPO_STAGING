#include "sfemul.hpp"

namespace sfemul {


uint64_t f16_to_f64_rm1(uint64_t v_arg)
{
    const uint64_t v_i = (uint64_t)(v_arg & UINT64_C(0x8000));
    const bool v__not_not = (v_i == UINT64_C(0x0));
    const uint64_t v__sh11 = (uint64_t)((uint64_t)(v_i) << ((UINT64_C(0x30)) & 63));
    const uint64_t v_i12 = v__sh11;
    const uint64_t v_i1 = (uint64_t)((uint64_t)(v_arg) >> ((UINT64_C(0xa)) & 63));
    const uint8_t v_i2 = (uint8_t)(v_i1);
    const uint8_t v_i3 = (uint8_t)(v_i2 & UINT32_C(0x1f));
    const uint16_t v_i4 = (uint16_t)(v_arg);
    const uint16_t v_i5 = (uint16_t)(v_i4 & UINT32_C(0x3ff));
    const bool v__q1 = (v_i3 == UINT32_C(0x1f));
    const bool v__q2 = (v_i3 == UINT32_C(0x0));
    const bool v_i7 = (v_i5 == UINT32_C(0x0));
    const uint64_t v__m7 = (uint64_t)((v_i7) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__m3 = (uint64_t)((v__not_not) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a4 = (uint64_t)(UINT64_C(0x7ff0000000000000) & v__m3);
    const uint64_t v__n5 = (uint64_t)(v__m3 ^ UINT64_C(0xffffffffffffffff));
    const uint64_t v__a6 = (uint64_t)(UINT64_C(0xfff0000000000000) & v__n5);
    const uint64_t v_i8 = (uint64_t)(v__a4 | v__a6);
    const uint64_t v__a8 = (uint64_t)(v_i8 & v__m7);
    const uint64_t v__n9 = (uint64_t)(v__m7 ^ UINT64_C(0xffffffffffffffff));
    const uint64_t v__a10 = (uint64_t)(UINT64_C(0x7ff8000000000000) & v__n9);
    const uint64_t v_spec_select = (uint64_t)(v__a8 | v__a10);
    const uint32_t v_i14 = (uint32_t)(v_i5);
    const uint32_t v__k12 = sf_ctlz32(v_i14);
    const uint32_t v_i15 = v__k12;
    const uint32_t v_i16 = (uint32_t)(v_i15 + UINT32_C(0xeb));
    const uint32_t v_i17 = (uint32_t)(v_i16 & UINT32_C(0xff));
    const uint32_t v__sh13 = (uint32_t)((uint32_t)(v_i14) << ((v_i17) & 31));
    const uint32_t v_i18 = v__sh13;
    const uint8_t v_i19 = (uint8_t)(v_i15);
    const uint16_t v_i20 = (uint16_t)(v_i18);
    const uint8_t v_i21 = (uint8_t)(UINT32_C(0x15) - v_i19);
    const bool v__n14 = (v_i7 != true);
    const bool v__c15 = (v__n14 && v__q2);
    const bool v__c37 = (v_i7 && v__q2);
    const bool v__c18 = (v__q1 || v__q2);
    const bool v__n19 = (v__c18 != true);
    const uint64_t v__m38 = (uint64_t)((v__c37) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a39 = (uint64_t)(v_i12 & v__m38);
    const uint64_t v__m41 = (uint64_t)((v__q1) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a42 = (uint64_t)(v_spec_select & v__m41);
    const uint16_t v__m16 = (uint16_t)((v__c15) ? ~(uint16_t)0 : (uint16_t)0);
    const uint16_t v__a17 = (uint16_t)(v_i20 & v__m16);
    const uint16_t v__m20 = (uint16_t)((v__n19) ? ~(uint16_t)0 : (uint16_t)0);
    const uint16_t v__a21 = (uint16_t)(v_i5 & v__m20);
    const uint16_t v__o22 = (uint16_t)(v__a17 | v__a21);
    const uint64_t v_i27 = (uint64_t)(v__o22);
    const uint64_t v__sh29 = (uint64_t)((uint64_t)(v_i27) << ((UINT64_C(0x2a)) & 63));
    const uint64_t v_i28 = v__sh29;
    const uint8_t v__m23 = (uint8_t)((v__c15) ? ~(uint8_t)0 : (uint8_t)0);
    const uint8_t v__a24 = (uint8_t)(v_i21 & v__m23);
    const bool v__c34 = (v__c15 || v__n19);
    const uint8_t v__m25 = (uint8_t)((v__n19) ? ~(uint8_t)0 : (uint8_t)0);
    const uint8_t v__a26 = (uint8_t)(v_i3 & v__m25);
    const uint8_t v__o27 = (uint8_t)(v__a24 | v__a26);
    const uint64_t v_i25 = (uint64_t)(int64_t)(int8_t)(v__o27);
    const uint64_t v__sh28 = (uint64_t)((uint64_t)(v_i25) << ((UINT64_C(0x34)) & 63));
    const uint64_t v_i26 = v__sh28;
    const uint64_t v__m35 = (uint64_t)((v__c34) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a31 = (uint64_t)(UINT64_C(0x3f00000000000000) & v__m3);
    const uint64_t v__a33 = (uint64_t)(UINT64_C(0xbf00000000000000) & v__n5);
    const uint64_t v_i29 = (uint64_t)(v__a31 | v__a33);
    const uint64_t v_i30 = (uint64_t)(v_i29 + v_i28);
    const uint64_t v_i31 = (uint64_t)(v_i30 + v_i26);
    const uint64_t v__a36 = (uint64_t)(v_i31 & v__m35);
    const uint64_t v__o40 = (uint64_t)(v__a36 | v__a39);
    const uint64_t v__o43 = (uint64_t)(v__o40 | v__a42);
    return v__o43;
}

}  // namespace sfemul
