// probe 0 -- compound assignment =
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_0(int32_t a, int32_t b)
{
    a = b;
    return a;
}

// probe 1 -- compound assignment =
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_1(int32_t a, int64_t b)
{
    a = b;
    return a;
}

// probe 2 -- compound assignment =
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_2(int32_t a, uint64_t b)
{
    a = b;
    return a;
}

// probe 3 -- compound assignment =
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_3(int32_t a, float b)
{
    a = b;
    return a;
}

// probe 4 -- compound assignment =
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_4(int32_t a, double b)
{
    a = b;
    return a;
}

// probe 5 -- compound assignment =
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_5(int32_t a, bool b)
{
    a = b;
    return a;
}

// probe 6 -- compound assignment =
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_6(int64_t a, int32_t b)
{
    a = b;
    return a;
}

// probe 7 -- compound assignment =
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_7(int64_t a, int64_t b)
{
    a = b;
    return a;
}

// probe 8 -- compound assignment =
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_8(int64_t a, uint64_t b)
{
    a = b;
    return a;
}

// probe 9 -- compound assignment =
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_9(int64_t a, float b)
{
    a = b;
    return a;
}

// probe 10 -- compound assignment =
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_10(int64_t a, double b)
{
    a = b;
    return a;
}

// probe 11 -- compound assignment =
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_11(int64_t a, bool b)
{
    a = b;
    return a;
}

// probe 12 -- compound assignment =
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_12(uint64_t a, int32_t b)
{
    a = b;
    return a;
}

// probe 13 -- compound assignment =
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_13(uint64_t a, int64_t b)
{
    a = b;
    return a;
}

// probe 14 -- compound assignment =
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_14(uint64_t a, uint64_t b)
{
    a = b;
    return a;
}

// probe 15 -- compound assignment =
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_15(uint64_t a, float b)
{
    a = b;
    return a;
}

// probe 16 -- compound assignment =
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_16(uint64_t a, double b)
{
    a = b;
    return a;
}

// probe 17 -- compound assignment =
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_17(uint64_t a, bool b)
{
    a = b;
    return a;
}

// probe 18 -- compound assignment =
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_18(float a, int32_t b)
{
    a = b;
    return a;
}

// probe 19 -- compound assignment =
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_19(float a, int64_t b)
{
    a = b;
    return a;
}

// probe 20 -- compound assignment =
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_20(float a, uint64_t b)
{
    a = b;
    return a;
}

// probe 21 -- compound assignment =
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_21(float a, float b)
{
    a = b;
    return a;
}

// probe 22 -- compound assignment =
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_22(float a, double b)
{
    a = b;
    return a;
}

// probe 23 -- compound assignment =
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_23(float a, bool b)
{
    a = b;
    return a;
}

// probe 24 -- compound assignment =
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_24(double a, int32_t b)
{
    a = b;
    return a;
}

// probe 25 -- compound assignment =
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_25(double a, int64_t b)
{
    a = b;
    return a;
}

// probe 26 -- compound assignment =
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_26(double a, uint64_t b)
{
    a = b;
    return a;
}

// probe 27 -- compound assignment =
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_27(double a, float b)
{
    a = b;
    return a;
}

// probe 28 -- compound assignment =
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_28(double a, double b)
{
    a = b;
    return a;
}

// probe 29 -- compound assignment =
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_29(double a, bool b)
{
    a = b;
    return a;
}

// probe 30 -- compound assignment =
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_30(bool a, int32_t b)
{
    a = b;
    return a;
}

// probe 31 -- compound assignment =
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_31(bool a, int64_t b)
{
    a = b;
    return a;
}

// probe 32 -- compound assignment =
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_32(bool a, uint64_t b)
{
    a = b;
    return a;
}

// probe 33 -- compound assignment =
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_33(bool a, float b)
{
    a = b;
    return a;
}

// probe 34 -- compound assignment =
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_34(bool a, double b)
{
    a = b;
    return a;
}

// probe 35 -- compound assignment =
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_35(bool a, bool b)
{
    a = b;
    return a;
}

// probe 36 -- compound assignment *=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_36(int32_t a, int32_t b)
{
    a *= b;
    return a;
}

// probe 37 -- compound assignment *=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_37(int32_t a, int64_t b)
{
    a *= b;
    return a;
}

// probe 38 -- compound assignment *=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_38(int32_t a, uint64_t b)
{
    a *= b;
    return a;
}

// probe 39 -- compound assignment *=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_39(int32_t a, float b)
{
    a *= b;
    return a;
}

// probe 40 -- compound assignment *=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_40(int32_t a, double b)
{
    a *= b;
    return a;
}

// probe 41 -- compound assignment *=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_41(int32_t a, bool b)
{
    a *= b;
    return a;
}

// probe 42 -- compound assignment *=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_42(int64_t a, int32_t b)
{
    a *= b;
    return a;
}

// probe 43 -- compound assignment *=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_43(int64_t a, int64_t b)
{
    a *= b;
    return a;
}

// probe 44 -- compound assignment *=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_44(int64_t a, uint64_t b)
{
    a *= b;
    return a;
}

// probe 45 -- compound assignment *=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_45(int64_t a, float b)
{
    a *= b;
    return a;
}

// probe 46 -- compound assignment *=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_46(int64_t a, double b)
{
    a *= b;
    return a;
}

// probe 47 -- compound assignment *=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_47(int64_t a, bool b)
{
    a *= b;
    return a;
}

// probe 48 -- compound assignment *=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_48(uint64_t a, int32_t b)
{
    a *= b;
    return a;
}

// probe 49 -- compound assignment *=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_49(uint64_t a, int64_t b)
{
    a *= b;
    return a;
}

// probe 50 -- compound assignment *=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_50(uint64_t a, uint64_t b)
{
    a *= b;
    return a;
}

// probe 51 -- compound assignment *=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_51(uint64_t a, float b)
{
    a *= b;
    return a;
}

// probe 52 -- compound assignment *=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_52(uint64_t a, double b)
{
    a *= b;
    return a;
}

// probe 53 -- compound assignment *=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_53(uint64_t a, bool b)
{
    a *= b;
    return a;
}

// probe 54 -- compound assignment *=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_54(float a, int32_t b)
{
    a *= b;
    return a;
}

// probe 55 -- compound assignment *=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_55(float a, int64_t b)
{
    a *= b;
    return a;
}

// probe 56 -- compound assignment *=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_56(float a, uint64_t b)
{
    a *= b;
    return a;
}

// probe 57 -- compound assignment *=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_57(float a, float b)
{
    a *= b;
    return a;
}

// probe 58 -- compound assignment *=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_58(float a, double b)
{
    a *= b;
    return a;
}

// probe 59 -- compound assignment *=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_59(float a, bool b)
{
    a *= b;
    return a;
}

// probe 60 -- compound assignment *=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_60(double a, int32_t b)
{
    a *= b;
    return a;
}

// probe 61 -- compound assignment *=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_61(double a, int64_t b)
{
    a *= b;
    return a;
}

// probe 62 -- compound assignment *=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_62(double a, uint64_t b)
{
    a *= b;
    return a;
}

// probe 63 -- compound assignment *=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_63(double a, float b)
{
    a *= b;
    return a;
}

// probe 64 -- compound assignment *=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_64(double a, double b)
{
    a *= b;
    return a;
}

// probe 65 -- compound assignment *=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_65(double a, bool b)
{
    a *= b;
    return a;
}

// probe 66 -- compound assignment *=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_66(bool a, int32_t b)
{
    a *= b;
    return a;
}

// probe 67 -- compound assignment *=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_67(bool a, int64_t b)
{
    a *= b;
    return a;
}

// probe 68 -- compound assignment *=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_68(bool a, uint64_t b)
{
    a *= b;
    return a;
}

// probe 69 -- compound assignment *=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_69(bool a, float b)
{
    a *= b;
    return a;
}

// probe 70 -- compound assignment *=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_70(bool a, double b)
{
    a *= b;
    return a;
}

// probe 71 -- compound assignment *=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_71(bool a, bool b)
{
    a *= b;
    return a;
}

// probe 72 -- compound assignment /=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_72(int32_t a, int32_t b)
{
    a /= b;
    return a;
}

// probe 73 -- compound assignment /=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_73(int32_t a, int64_t b)
{
    a /= b;
    return a;
}

// probe 74 -- compound assignment /=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_74(int32_t a, uint64_t b)
{
    a /= b;
    return a;
}

// probe 75 -- compound assignment /=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_75(int32_t a, float b)
{
    a /= b;
    return a;
}

// probe 76 -- compound assignment /=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_76(int32_t a, double b)
{
    a /= b;
    return a;
}

// probe 77 -- compound assignment /=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_77(int32_t a, bool b)
{
    a /= b;
    return a;
}

// probe 78 -- compound assignment /=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_78(int64_t a, int32_t b)
{
    a /= b;
    return a;
}

// probe 79 -- compound assignment /=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_79(int64_t a, int64_t b)
{
    a /= b;
    return a;
}

// probe 80 -- compound assignment /=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_80(int64_t a, uint64_t b)
{
    a /= b;
    return a;
}

// probe 81 -- compound assignment /=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_81(int64_t a, float b)
{
    a /= b;
    return a;
}

// probe 82 -- compound assignment /=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_82(int64_t a, double b)
{
    a /= b;
    return a;
}

// probe 83 -- compound assignment /=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_83(int64_t a, bool b)
{
    a /= b;
    return a;
}

// probe 84 -- compound assignment /=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_84(uint64_t a, int32_t b)
{
    a /= b;
    return a;
}

// probe 85 -- compound assignment /=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_85(uint64_t a, int64_t b)
{
    a /= b;
    return a;
}

// probe 86 -- compound assignment /=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_86(uint64_t a, uint64_t b)
{
    a /= b;
    return a;
}

// probe 87 -- compound assignment /=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_87(uint64_t a, float b)
{
    a /= b;
    return a;
}

// probe 88 -- compound assignment /=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_88(uint64_t a, double b)
{
    a /= b;
    return a;
}

// probe 89 -- compound assignment /=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_89(uint64_t a, bool b)
{
    a /= b;
    return a;
}

// probe 90 -- compound assignment /=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_90(float a, int32_t b)
{
    a /= b;
    return a;
}

// probe 91 -- compound assignment /=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_91(float a, int64_t b)
{
    a /= b;
    return a;
}

// probe 92 -- compound assignment /=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_92(float a, uint64_t b)
{
    a /= b;
    return a;
}

// probe 93 -- compound assignment /=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_93(float a, float b)
{
    a /= b;
    return a;
}

// probe 94 -- compound assignment /=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_94(float a, double b)
{
    a /= b;
    return a;
}

// probe 95 -- compound assignment /=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_95(float a, bool b)
{
    a /= b;
    return a;
}

// probe 96 -- compound assignment /=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_96(double a, int32_t b)
{
    a /= b;
    return a;
}

// probe 97 -- compound assignment /=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_97(double a, int64_t b)
{
    a /= b;
    return a;
}

// probe 98 -- compound assignment /=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_98(double a, uint64_t b)
{
    a /= b;
    return a;
}

// probe 99 -- compound assignment /=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_99(double a, float b)
{
    a /= b;
    return a;
}

// probe 100 -- compound assignment /=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_100(double a, double b)
{
    a /= b;
    return a;
}

// probe 101 -- compound assignment /=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_101(double a, bool b)
{
    a /= b;
    return a;
}

// probe 102 -- compound assignment /=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_102(bool a, int32_t b)
{
    a /= b;
    return a;
}

// probe 103 -- compound assignment /=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_103(bool a, int64_t b)
{
    a /= b;
    return a;
}

// probe 104 -- compound assignment /=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_104(bool a, uint64_t b)
{
    a /= b;
    return a;
}

// probe 105 -- compound assignment /=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_105(bool a, float b)
{
    a /= b;
    return a;
}

// probe 106 -- compound assignment /=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_106(bool a, double b)
{
    a /= b;
    return a;
}

// probe 107 -- compound assignment /=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_107(bool a, bool b)
{
    a /= b;
    return a;
}

// probe 108 -- compound assignment %=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_108(int32_t a, int32_t b)
{
    a %= b;
    return a;
}

// probe 109 -- compound assignment %=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_109(int32_t a, int64_t b)
{
    a %= b;
    return a;
}

// probe 110 -- compound assignment %=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_110(int32_t a, uint64_t b)
{
    a %= b;
    return a;
}

// probe 113 -- compound assignment %=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_113(int32_t a, bool b)
{
    a %= b;
    return a;
}

// probe 114 -- compound assignment %=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_114(int64_t a, int32_t b)
{
    a %= b;
    return a;
}

// probe 115 -- compound assignment %=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_115(int64_t a, int64_t b)
{
    a %= b;
    return a;
}

// probe 116 -- compound assignment %=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_116(int64_t a, uint64_t b)
{
    a %= b;
    return a;
}

// probe 119 -- compound assignment %=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_119(int64_t a, bool b)
{
    a %= b;
    return a;
}

// probe 120 -- compound assignment %=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_120(uint64_t a, int32_t b)
{
    a %= b;
    return a;
}

// probe 121 -- compound assignment %=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_121(uint64_t a, int64_t b)
{
    a %= b;
    return a;
}

// probe 122 -- compound assignment %=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_122(uint64_t a, uint64_t b)
{
    a %= b;
    return a;
}

// probe 125 -- compound assignment %=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_125(uint64_t a, bool b)
{
    a %= b;
    return a;
}

// probe 138 -- compound assignment %=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_138(bool a, int32_t b)
{
    a %= b;
    return a;
}

// probe 139 -- compound assignment %=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_139(bool a, int64_t b)
{
    a %= b;
    return a;
}

// probe 140 -- compound assignment %=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_140(bool a, uint64_t b)
{
    a %= b;
    return a;
}

// probe 143 -- compound assignment %=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_143(bool a, bool b)
{
    a %= b;
    return a;
}

// probe 144 -- compound assignment +=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_144(int32_t a, int32_t b)
{
    a += b;
    return a;
}

// probe 145 -- compound assignment +=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_145(int32_t a, int64_t b)
{
    a += b;
    return a;
}

// probe 146 -- compound assignment +=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_146(int32_t a, uint64_t b)
{
    a += b;
    return a;
}

// probe 147 -- compound assignment +=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_147(int32_t a, float b)
{
    a += b;
    return a;
}

// probe 148 -- compound assignment +=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_148(int32_t a, double b)
{
    a += b;
    return a;
}

// probe 149 -- compound assignment +=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_149(int32_t a, bool b)
{
    a += b;
    return a;
}

// probe 150 -- compound assignment +=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_150(int64_t a, int32_t b)
{
    a += b;
    return a;
}

// probe 151 -- compound assignment +=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_151(int64_t a, int64_t b)
{
    a += b;
    return a;
}

// probe 152 -- compound assignment +=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_152(int64_t a, uint64_t b)
{
    a += b;
    return a;
}

// probe 153 -- compound assignment +=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_153(int64_t a, float b)
{
    a += b;
    return a;
}

// probe 154 -- compound assignment +=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_154(int64_t a, double b)
{
    a += b;
    return a;
}

// probe 155 -- compound assignment +=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_155(int64_t a, bool b)
{
    a += b;
    return a;
}

// probe 156 -- compound assignment +=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_156(uint64_t a, int32_t b)
{
    a += b;
    return a;
}

// probe 157 -- compound assignment +=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_157(uint64_t a, int64_t b)
{
    a += b;
    return a;
}

// probe 158 -- compound assignment +=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_158(uint64_t a, uint64_t b)
{
    a += b;
    return a;
}

// probe 159 -- compound assignment +=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_159(uint64_t a, float b)
{
    a += b;
    return a;
}

// probe 160 -- compound assignment +=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_160(uint64_t a, double b)
{
    a += b;
    return a;
}

// probe 161 -- compound assignment +=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_161(uint64_t a, bool b)
{
    a += b;
    return a;
}

// probe 162 -- compound assignment +=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_162(float a, int32_t b)
{
    a += b;
    return a;
}

// probe 163 -- compound assignment +=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_163(float a, int64_t b)
{
    a += b;
    return a;
}

// probe 164 -- compound assignment +=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_164(float a, uint64_t b)
{
    a += b;
    return a;
}

// probe 165 -- compound assignment +=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_165(float a, float b)
{
    a += b;
    return a;
}

// probe 166 -- compound assignment +=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_166(float a, double b)
{
    a += b;
    return a;
}

// probe 167 -- compound assignment +=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_167(float a, bool b)
{
    a += b;
    return a;
}

// probe 168 -- compound assignment +=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_168(double a, int32_t b)
{
    a += b;
    return a;
}

// probe 169 -- compound assignment +=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_169(double a, int64_t b)
{
    a += b;
    return a;
}

// probe 170 -- compound assignment +=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_170(double a, uint64_t b)
{
    a += b;
    return a;
}

// probe 171 -- compound assignment +=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_171(double a, float b)
{
    a += b;
    return a;
}

// probe 172 -- compound assignment +=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_172(double a, double b)
{
    a += b;
    return a;
}

// probe 173 -- compound assignment +=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_173(double a, bool b)
{
    a += b;
    return a;
}

// probe 174 -- compound assignment +=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_174(bool a, int32_t b)
{
    a += b;
    return a;
}

// probe 175 -- compound assignment +=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_175(bool a, int64_t b)
{
    a += b;
    return a;
}

// probe 176 -- compound assignment +=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_176(bool a, uint64_t b)
{
    a += b;
    return a;
}

// probe 177 -- compound assignment +=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_177(bool a, float b)
{
    a += b;
    return a;
}

// probe 178 -- compound assignment +=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_178(bool a, double b)
{
    a += b;
    return a;
}

// probe 179 -- compound assignment +=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_179(bool a, bool b)
{
    a += b;
    return a;
}

// probe 180 -- compound assignment -=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_180(int32_t a, int32_t b)
{
    a -= b;
    return a;
}

// probe 181 -- compound assignment -=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_181(int32_t a, int64_t b)
{
    a -= b;
    return a;
}

// probe 182 -- compound assignment -=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_182(int32_t a, uint64_t b)
{
    a -= b;
    return a;
}

// probe 183 -- compound assignment -=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_183(int32_t a, float b)
{
    a -= b;
    return a;
}

// probe 184 -- compound assignment -=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_184(int32_t a, double b)
{
    a -= b;
    return a;
}

// probe 185 -- compound assignment -=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_185(int32_t a, bool b)
{
    a -= b;
    return a;
}

// probe 186 -- compound assignment -=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_186(int64_t a, int32_t b)
{
    a -= b;
    return a;
}

// probe 187 -- compound assignment -=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_187(int64_t a, int64_t b)
{
    a -= b;
    return a;
}

// probe 188 -- compound assignment -=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_188(int64_t a, uint64_t b)
{
    a -= b;
    return a;
}

// probe 189 -- compound assignment -=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_189(int64_t a, float b)
{
    a -= b;
    return a;
}

// probe 190 -- compound assignment -=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_190(int64_t a, double b)
{
    a -= b;
    return a;
}

// probe 191 -- compound assignment -=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_191(int64_t a, bool b)
{
    a -= b;
    return a;
}

// probe 192 -- compound assignment -=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_192(uint64_t a, int32_t b)
{
    a -= b;
    return a;
}

// probe 193 -- compound assignment -=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_193(uint64_t a, int64_t b)
{
    a -= b;
    return a;
}

// probe 194 -- compound assignment -=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_194(uint64_t a, uint64_t b)
{
    a -= b;
    return a;
}

// probe 195 -- compound assignment -=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_195(uint64_t a, float b)
{
    a -= b;
    return a;
}

// probe 196 -- compound assignment -=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_196(uint64_t a, double b)
{
    a -= b;
    return a;
}

// probe 197 -- compound assignment -=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_197(uint64_t a, bool b)
{
    a -= b;
    return a;
}

// probe 198 -- compound assignment -=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_198(float a, int32_t b)
{
    a -= b;
    return a;
}

// probe 199 -- compound assignment -=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_199(float a, int64_t b)
{
    a -= b;
    return a;
}

// probe 200 -- compound assignment -=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_200(float a, uint64_t b)
{
    a -= b;
    return a;
}

// probe 201 -- compound assignment -=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_201(float a, float b)
{
    a -= b;
    return a;
}

// probe 202 -- compound assignment -=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_202(float a, double b)
{
    a -= b;
    return a;
}

// probe 203 -- compound assignment -=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_203(float a, bool b)
{
    a -= b;
    return a;
}

// probe 204 -- compound assignment -=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_204(double a, int32_t b)
{
    a -= b;
    return a;
}

// probe 205 -- compound assignment -=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_205(double a, int64_t b)
{
    a -= b;
    return a;
}

// probe 206 -- compound assignment -=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_206(double a, uint64_t b)
{
    a -= b;
    return a;
}

// probe 207 -- compound assignment -=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_207(double a, float b)
{
    a -= b;
    return a;
}

// probe 208 -- compound assignment -=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_208(double a, double b)
{
    a -= b;
    return a;
}

// probe 209 -- compound assignment -=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_209(double a, bool b)
{
    a -= b;
    return a;
}

// probe 210 -- compound assignment -=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_210(bool a, int32_t b)
{
    a -= b;
    return a;
}

// probe 211 -- compound assignment -=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_211(bool a, int64_t b)
{
    a -= b;
    return a;
}

// probe 212 -- compound assignment -=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_212(bool a, uint64_t b)
{
    a -= b;
    return a;
}

// probe 213 -- compound assignment -=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_213(bool a, float b)
{
    a -= b;
    return a;
}

// probe 214 -- compound assignment -=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_214(bool a, double b)
{
    a -= b;
    return a;
}

// probe 215 -- compound assignment -=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_215(bool a, bool b)
{
    a -= b;
    return a;
}

// probe 216 -- compound assignment <<=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_216(int32_t a, int32_t b)
{
    a <<= b;
    return a;
}

// probe 217 -- compound assignment <<=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_217(int32_t a, int64_t b)
{
    a <<= b;
    return a;
}

// probe 218 -- compound assignment <<=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_218(int32_t a, uint64_t b)
{
    a <<= b;
    return a;
}

// probe 221 -- compound assignment <<=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_221(int32_t a, bool b)
{
    a <<= b;
    return a;
}

// probe 222 -- compound assignment <<=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_222(int64_t a, int32_t b)
{
    a <<= b;
    return a;
}

// probe 223 -- compound assignment <<=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_223(int64_t a, int64_t b)
{
    a <<= b;
    return a;
}

// probe 224 -- compound assignment <<=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_224(int64_t a, uint64_t b)
{
    a <<= b;
    return a;
}

// probe 227 -- compound assignment <<=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_227(int64_t a, bool b)
{
    a <<= b;
    return a;
}

// probe 228 -- compound assignment <<=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_228(uint64_t a, int32_t b)
{
    a <<= b;
    return a;
}

// probe 229 -- compound assignment <<=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_229(uint64_t a, int64_t b)
{
    a <<= b;
    return a;
}

// probe 230 -- compound assignment <<=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_230(uint64_t a, uint64_t b)
{
    a <<= b;
    return a;
}

// probe 233 -- compound assignment <<=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_233(uint64_t a, bool b)
{
    a <<= b;
    return a;
}

// probe 246 -- compound assignment <<=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_246(bool a, int32_t b)
{
    a <<= b;
    return a;
}

// probe 247 -- compound assignment <<=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_247(bool a, int64_t b)
{
    a <<= b;
    return a;
}

// probe 248 -- compound assignment <<=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_248(bool a, uint64_t b)
{
    a <<= b;
    return a;
}

// probe 251 -- compound assignment <<=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_251(bool a, bool b)
{
    a <<= b;
    return a;
}

// probe 252 -- compound assignment >>=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_252(int32_t a, int32_t b)
{
    a >>= b;
    return a;
}

// probe 253 -- compound assignment >>=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_253(int32_t a, int64_t b)
{
    a >>= b;
    return a;
}

// probe 254 -- compound assignment >>=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_254(int32_t a, uint64_t b)
{
    a >>= b;
    return a;
}

// probe 257 -- compound assignment >>=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_257(int32_t a, bool b)
{
    a >>= b;
    return a;
}

// probe 258 -- compound assignment >>=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_258(int64_t a, int32_t b)
{
    a >>= b;
    return a;
}

// probe 259 -- compound assignment >>=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_259(int64_t a, int64_t b)
{
    a >>= b;
    return a;
}

// probe 260 -- compound assignment >>=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_260(int64_t a, uint64_t b)
{
    a >>= b;
    return a;
}

// probe 263 -- compound assignment >>=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_263(int64_t a, bool b)
{
    a >>= b;
    return a;
}

// probe 264 -- compound assignment >>=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_264(uint64_t a, int32_t b)
{
    a >>= b;
    return a;
}

// probe 265 -- compound assignment >>=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_265(uint64_t a, int64_t b)
{
    a >>= b;
    return a;
}

// probe 266 -- compound assignment >>=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_266(uint64_t a, uint64_t b)
{
    a >>= b;
    return a;
}

// probe 269 -- compound assignment >>=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_269(uint64_t a, bool b)
{
    a >>= b;
    return a;
}

// probe 282 -- compound assignment >>=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_282(bool a, int32_t b)
{
    a >>= b;
    return a;
}

// probe 283 -- compound assignment >>=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_283(bool a, int64_t b)
{
    a >>= b;
    return a;
}

// probe 284 -- compound assignment >>=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_284(bool a, uint64_t b)
{
    a >>= b;
    return a;
}

// probe 287 -- compound assignment >>=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_287(bool a, bool b)
{
    a >>= b;
    return a;
}

// probe 288 -- compound assignment &=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_288(int32_t a, int32_t b)
{
    a &= b;
    return a;
}

// probe 289 -- compound assignment &=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_289(int32_t a, int64_t b)
{
    a &= b;
    return a;
}

// probe 290 -- compound assignment &=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_290(int32_t a, uint64_t b)
{
    a &= b;
    return a;
}

// probe 293 -- compound assignment &=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_293(int32_t a, bool b)
{
    a &= b;
    return a;
}

// probe 294 -- compound assignment &=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_294(int64_t a, int32_t b)
{
    a &= b;
    return a;
}

// probe 295 -- compound assignment &=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_295(int64_t a, int64_t b)
{
    a &= b;
    return a;
}

// probe 296 -- compound assignment &=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_296(int64_t a, uint64_t b)
{
    a &= b;
    return a;
}

// probe 299 -- compound assignment &=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_299(int64_t a, bool b)
{
    a &= b;
    return a;
}

// probe 300 -- compound assignment &=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_300(uint64_t a, int32_t b)
{
    a &= b;
    return a;
}

// probe 301 -- compound assignment &=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_301(uint64_t a, int64_t b)
{
    a &= b;
    return a;
}

// probe 302 -- compound assignment &=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_302(uint64_t a, uint64_t b)
{
    a &= b;
    return a;
}

// probe 305 -- compound assignment &=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_305(uint64_t a, bool b)
{
    a &= b;
    return a;
}

// probe 318 -- compound assignment &=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_318(bool a, int32_t b)
{
    a &= b;
    return a;
}

// probe 319 -- compound assignment &=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_319(bool a, int64_t b)
{
    a &= b;
    return a;
}

// probe 320 -- compound assignment &=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_320(bool a, uint64_t b)
{
    a &= b;
    return a;
}

// probe 323 -- compound assignment &=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_323(bool a, bool b)
{
    a &= b;
    return a;
}

// probe 324 -- compound assignment ^=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_324(int32_t a, int32_t b)
{
    a ^= b;
    return a;
}

// probe 325 -- compound assignment ^=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_325(int32_t a, int64_t b)
{
    a ^= b;
    return a;
}

// probe 326 -- compound assignment ^=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_326(int32_t a, uint64_t b)
{
    a ^= b;
    return a;
}

// probe 329 -- compound assignment ^=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_329(int32_t a, bool b)
{
    a ^= b;
    return a;
}

// probe 330 -- compound assignment ^=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_330(int64_t a, int32_t b)
{
    a ^= b;
    return a;
}

// probe 331 -- compound assignment ^=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_331(int64_t a, int64_t b)
{
    a ^= b;
    return a;
}

// probe 332 -- compound assignment ^=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_332(int64_t a, uint64_t b)
{
    a ^= b;
    return a;
}

// probe 335 -- compound assignment ^=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_335(int64_t a, bool b)
{
    a ^= b;
    return a;
}

// probe 336 -- compound assignment ^=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_336(uint64_t a, int32_t b)
{
    a ^= b;
    return a;
}

// probe 337 -- compound assignment ^=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_337(uint64_t a, int64_t b)
{
    a ^= b;
    return a;
}

// probe 338 -- compound assignment ^=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_338(uint64_t a, uint64_t b)
{
    a ^= b;
    return a;
}

// probe 341 -- compound assignment ^=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_341(uint64_t a, bool b)
{
    a ^= b;
    return a;
}

// probe 354 -- compound assignment ^=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_354(bool a, int32_t b)
{
    a ^= b;
    return a;
}

// probe 355 -- compound assignment ^=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_355(bool a, int64_t b)
{
    a ^= b;
    return a;
}

// probe 356 -- compound assignment ^=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_356(bool a, uint64_t b)
{
    a ^= b;
    return a;
}

// probe 359 -- compound assignment ^=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_359(bool a, bool b)
{
    a ^= b;
    return a;
}

// probe 360 -- compound assignment |=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_360(int32_t a, int32_t b)
{
    a |= b;
    return a;
}

// probe 361 -- compound assignment |=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_361(int32_t a, int64_t b)
{
    a |= b;
    return a;
}

// probe 362 -- compound assignment |=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_362(int32_t a, uint64_t b)
{
    a |= b;
    return a;
}

// probe 365 -- compound assignment |=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_365(int32_t a, bool b)
{
    a |= b;
    return a;
}

// probe 366 -- compound assignment |=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_366(int64_t a, int32_t b)
{
    a |= b;
    return a;
}

// probe 367 -- compound assignment |=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_367(int64_t a, int64_t b)
{
    a |= b;
    return a;
}

// probe 368 -- compound assignment |=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_368(int64_t a, uint64_t b)
{
    a |= b;
    return a;
}

// probe 371 -- compound assignment |=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_371(int64_t a, bool b)
{
    a |= b;
    return a;
}

// probe 372 -- compound assignment |=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_372(uint64_t a, int32_t b)
{
    a |= b;
    return a;
}

// probe 373 -- compound assignment |=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_373(uint64_t a, int64_t b)
{
    a |= b;
    return a;
}

// probe 374 -- compound assignment |=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_374(uint64_t a, uint64_t b)
{
    a |= b;
    return a;
}

// probe 377 -- compound assignment |=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_377(uint64_t a, bool b)
{
    a |= b;
    return a;
}

// probe 390 -- compound assignment |=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_390(bool a, int32_t b)
{
    a |= b;
    return a;
}

// probe 391 -- compound assignment |=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_391(bool a, int64_t b)
{
    a |= b;
    return a;
}

// probe 392 -- compound assignment |=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_392(bool a, uint64_t b)
{
    a |= b;
    return a;
}

// probe 395 -- compound assignment |=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_395(bool a, bool b)
{
    a |= b;
    return a;
}

// probe 396 -- compound assignment and_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_396(int32_t a, int32_t b)
{
    a and_eq b;
    return a;
}

// probe 397 -- compound assignment and_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_397(int32_t a, int64_t b)
{
    a and_eq b;
    return a;
}

// probe 398 -- compound assignment and_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_398(int32_t a, uint64_t b)
{
    a and_eq b;
    return a;
}

// probe 401 -- compound assignment and_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_401(int32_t a, bool b)
{
    a and_eq b;
    return a;
}

// probe 402 -- compound assignment and_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_402(int64_t a, int32_t b)
{
    a and_eq b;
    return a;
}

// probe 403 -- compound assignment and_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_403(int64_t a, int64_t b)
{
    a and_eq b;
    return a;
}

// probe 404 -- compound assignment and_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_404(int64_t a, uint64_t b)
{
    a and_eq b;
    return a;
}

// probe 407 -- compound assignment and_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_407(int64_t a, bool b)
{
    a and_eq b;
    return a;
}

// probe 408 -- compound assignment and_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_408(uint64_t a, int32_t b)
{
    a and_eq b;
    return a;
}

// probe 409 -- compound assignment and_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_409(uint64_t a, int64_t b)
{
    a and_eq b;
    return a;
}

// probe 410 -- compound assignment and_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_410(uint64_t a, uint64_t b)
{
    a and_eq b;
    return a;
}

// probe 413 -- compound assignment and_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_413(uint64_t a, bool b)
{
    a and_eq b;
    return a;
}

// probe 426 -- compound assignment and_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_426(bool a, int32_t b)
{
    a and_eq b;
    return a;
}

// probe 427 -- compound assignment and_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_427(bool a, int64_t b)
{
    a and_eq b;
    return a;
}

// probe 428 -- compound assignment and_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_428(bool a, uint64_t b)
{
    a and_eq b;
    return a;
}

// probe 431 -- compound assignment and_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_431(bool a, bool b)
{
    a and_eq b;
    return a;
}

// probe 432 -- compound assignment or_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_432(int32_t a, int32_t b)
{
    a or_eq b;
    return a;
}

// probe 433 -- compound assignment or_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_433(int32_t a, int64_t b)
{
    a or_eq b;
    return a;
}

// probe 434 -- compound assignment or_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_434(int32_t a, uint64_t b)
{
    a or_eq b;
    return a;
}

// probe 437 -- compound assignment or_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_437(int32_t a, bool b)
{
    a or_eq b;
    return a;
}

// probe 438 -- compound assignment or_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_438(int64_t a, int32_t b)
{
    a or_eq b;
    return a;
}

// probe 439 -- compound assignment or_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_439(int64_t a, int64_t b)
{
    a or_eq b;
    return a;
}

// probe 440 -- compound assignment or_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_440(int64_t a, uint64_t b)
{
    a or_eq b;
    return a;
}

// probe 443 -- compound assignment or_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_443(int64_t a, bool b)
{
    a or_eq b;
    return a;
}

// probe 444 -- compound assignment or_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_444(uint64_t a, int32_t b)
{
    a or_eq b;
    return a;
}

// probe 445 -- compound assignment or_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_445(uint64_t a, int64_t b)
{
    a or_eq b;
    return a;
}

// probe 446 -- compound assignment or_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_446(uint64_t a, uint64_t b)
{
    a or_eq b;
    return a;
}

// probe 449 -- compound assignment or_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_449(uint64_t a, bool b)
{
    a or_eq b;
    return a;
}

// probe 462 -- compound assignment or_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_462(bool a, int32_t b)
{
    a or_eq b;
    return a;
}

// probe 463 -- compound assignment or_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_463(bool a, int64_t b)
{
    a or_eq b;
    return a;
}

// probe 464 -- compound assignment or_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_464(bool a, uint64_t b)
{
    a or_eq b;
    return a;
}

// probe 467 -- compound assignment or_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_467(bool a, bool b)
{
    a or_eq b;
    return a;
}

// probe 468 -- compound assignment xor_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_468(int32_t a, int32_t b)
{
    a xor_eq b;
    return a;
}

// probe 469 -- compound assignment xor_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_469(int32_t a, int64_t b)
{
    a xor_eq b;
    return a;
}

// probe 470 -- compound assignment xor_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_470(int32_t a, uint64_t b)
{
    a xor_eq b;
    return a;
}

// probe 473 -- compound assignment xor_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_473(int32_t a, bool b)
{
    a xor_eq b;
    return a;
}

// probe 474 -- compound assignment xor_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_474(int64_t a, int32_t b)
{
    a xor_eq b;
    return a;
}

// probe 475 -- compound assignment xor_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_475(int64_t a, int64_t b)
{
    a xor_eq b;
    return a;
}

// probe 476 -- compound assignment xor_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_476(int64_t a, uint64_t b)
{
    a xor_eq b;
    return a;
}

// probe 479 -- compound assignment xor_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_479(int64_t a, bool b)
{
    a xor_eq b;
    return a;
}

// probe 480 -- compound assignment xor_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_480(uint64_t a, int32_t b)
{
    a xor_eq b;
    return a;
}

// probe 481 -- compound assignment xor_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_481(uint64_t a, int64_t b)
{
    a xor_eq b;
    return a;
}

// probe 482 -- compound assignment xor_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_482(uint64_t a, uint64_t b)
{
    a xor_eq b;
    return a;
}

// probe 485 -- compound assignment xor_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_485(uint64_t a, bool b)
{
    a xor_eq b;
    return a;
}

// probe 498 -- compound assignment xor_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_498(bool a, int32_t b)
{
    a xor_eq b;
    return a;
}

// probe 499 -- compound assignment xor_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_499(bool a, int64_t b)
{
    a xor_eq b;
    return a;
}

// probe 500 -- compound assignment xor_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_500(bool a, uint64_t b)
{
    a xor_eq b;
    return a;
}

// probe 503 -- compound assignment xor_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_503(bool a, bool b)
{
    a xor_eq b;
    return a;
}
