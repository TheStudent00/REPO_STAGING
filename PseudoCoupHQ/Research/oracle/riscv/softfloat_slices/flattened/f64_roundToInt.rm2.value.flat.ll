; ModuleID = '<scratch>/fl/run/f64_roundToInt.rm2.value/f64_roundToInt.rm2.value.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local i64 @f64_roundToInt_rm2_value_flat(i64 %arg, i1 noundef zeroext %arg1) {
  %i = lshr i64 %arg, 52
  %i2 = trunc i64 %i to i32
  %i3 = and i32 %i2, 2047
  %i4 = icmp ult i32 %i3, 1023
  %i11 = icmp ugt i32 %i3, 1074
  %i6 = and i64 %arg, 9223372036854775807
  %i7 = icmp eq i64 %i6, 0
  %i13 = icmp ne i32 %i3, 2047
  %i18 = sub i32 1075, %i3
  %i19 = zext i32 %i18 to i64
  %.sh5 = shl i64 1, %i19
  %i20 = freeze i64 %.sh5
  %i14 = and i64 %arg, 4503599627370495
  %i15 = icmp eq i64 %i14, 0
  %i16 = or i1 %i15, %i13
  %.m1 = sext i1 %i16 to i64
  %.a2 = and i64 %arg, %.m1
  %.n3 = xor i64 %.m1, -1
  %.a4 = and i64 9221120237041090560, %.n3
  %spec.select = or i64 %.a2, %.a4
  %i21 = add i64 %i20, -1
  %i25 = sub i64 0, %i20
  %i22 = icmp slt i64 %arg, 0
  %.m6 = sext i1 %i22 to i64
  %i23 = and i64 %i21, %.m6
  %i24 = add i64 %i23, %arg
  %i26 = and i64 %i24, %i25
  %i9 = and i64 -4616189618054758400, %.m6
  %.c8 = and i1 %i7, %i4
  %.m9 = sext i1 %.c8 to i64
  %.a10 = and i64 %arg, %.m9
  %.n11 = xor i1 %i7, true
  %.c12 = and i1 %.n11, %i4
  %.m13 = sext i1 %.c12 to i64
  %.a14 = and i64 %i9, %.m13
  %.o15 = or i64 %.a10, %.a14
  %.n16 = xor i1 %i4, true
  %.n17 = xor i1 %i11, true
  %.c18 = and i1 %.n16, %.n17
  %.m19 = sext i1 %.c18 to i64
  %.a20 = and i64 %i26, %.m19
  %.o21 = or i64 %.o15, %.a20
  %.m23 = sext i1 %i11 to i64
  %.a24 = and i64 %spec.select, %.m23
  %.o25 = or i64 %.o21, %.a24
  ret i64 %.o25
}

!llvm.ident = !{!0, !0, !0, !0, !0, !0, !0}
!llvm.module.flags = !{!1, !2, !3, !5}

!0 = !{!"Ubuntu clang version 21.1.8 (6ubuntu1)"}
!1 = !{i32 1, !"wchar_size", i32 4}
!2 = !{i32 1, !"target-abi", !"lp64"}
!3 = distinct !{i32 6, !"riscv-isa", !4}
!4 = distinct !{!"rv64i2p1_m2p0_zmmul1p0"}
!5 = !{i32 8, !"SmallDataLimit", i32 0}
