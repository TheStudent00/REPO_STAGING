; ModuleID = '<scratch>/fl/run/f64_roundToInt.rm4.value/f64_roundToInt.rm4.value.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local i64 @f64_roundToInt_rm4_value_flat(i64 %arg, i1 noundef zeroext %arg1) {
  %i = lshr i64 %arg, 52
  %i2 = trunc i64 %i to i32
  %i3 = and i32 %i2, 2047
  %i4 = icmp ult i32 %i3, 1023
  %i13 = icmp ugt i32 %i3, 1074
  %i6 = and i64 %arg, 9223372036854775807
  %i7 = icmp eq i64 %i6, 0
  %i15 = icmp ne i32 %i3, 2047
  %i16 = and i64 %arg, 4503599627370495
  %i17 = icmp eq i64 %i16, 0
  %i18 = or i1 %i17, %i15
  %.m1 = sext i1 %i18 to i64
  %.a2 = and i64 %arg, %.m1
  %.n3 = xor i64 %.m1, -1
  %.a4 = and i64 9221120237041090560, %.n3
  %spec.select4 = or i64 %.a2, %.a4
  %i20 = sub i32 1075, %i3
  %i21 = zext i32 %i20 to i64
  %.sh5 = shl i64 1, %i21
  %i22 = freeze i64 %.sh5
  %i10 = icmp eq i32 %i3, 1022
  %.m7 = sext i1 %i10 to i64
  %.sh6 = lshr i64 %i22, 1
  %i24 = add i64 %.sh6, %arg
  %i25 = sub i64 0, %i22
  %i26 = and i64 %i24, %i25
  %i9 = and i64 %arg, -9223372036854775808
  %i11 = or i64 %i9, 4607182418800017408
  %.a8 = and i64 %i11, %.m7
  %.n9 = xor i64 %.m7, -1
  %.a10 = and i64 %i9, %.n9
  %spec.select = or i64 %.a8, %.a10
  %.c11 = and i1 %i7, %i4
  %.m12 = sext i1 %.c11 to i64
  %.a13 = and i64 %arg, %.m12
  %.n14 = xor i1 %i7, true
  %.c15 = and i1 %.n14, %i4
  %.m16 = sext i1 %.c15 to i64
  %.a17 = and i64 %spec.select, %.m16
  %.o18 = or i64 %.a13, %.a17
  %.n19 = xor i1 %i4, true
  %.n20 = xor i1 %i13, true
  %.c21 = and i1 %.n19, %.n20
  %.m22 = sext i1 %.c21 to i64
  %.a23 = and i64 %i26, %.m22
  %.o24 = or i64 %.o18, %.a23
  %.m26 = sext i1 %i13 to i64
  %.a27 = and i64 %spec.select4, %.m26
  %.o28 = or i64 %.o24, %.a27
  ret i64 %.o28
}

!llvm.ident = !{!0, !0, !0, !0, !0, !0, !0}
!llvm.module.flags = !{!1, !2, !3, !5}

!0 = !{!"Ubuntu clang version 21.1.8 (6ubuntu1)"}
!1 = !{i32 1, !"wchar_size", i32 4}
!2 = !{i32 1, !"target-abi", !"lp64"}
!3 = distinct !{i32 6, !"riscv-isa", !4}
!4 = distinct !{!"rv64i2p1_m2p0_zmmul1p0"}
!5 = !{i32 8, !"SmallDataLimit", i32 0}
