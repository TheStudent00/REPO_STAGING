; ModuleID = '<scratch>/fl/run/f64_roundToInt.rm1.value/f64_roundToInt.rm1.value.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local i64 @f64_roundToInt_rm1_value_flat(i64 %arg, i1 noundef zeroext %arg1) {
  %i = lshr i64 %arg, 52
  %i2 = trunc i64 %i to i32
  %i3 = and i32 %i2, 2047
  %i4 = icmp ult i32 %i3, 1023
  %i6 = and i64 %arg, 9223372036854775807
  %i7 = icmp eq i64 %i6, 0
  %.m1 = sext i1 %i7 to i64
  %i8 = and i64 %arg, -9223372036854775808
  %.a2 = and i64 %arg, %.m1
  %.n3 = xor i64 %.m1, -1
  %.a4 = and i64 %i8, %.n3
  %spec.select = or i64 %.a2, %.a4
  %i10 = icmp ugt i32 %i3, 1074
  %i12 = icmp ne i32 %i3, 2047
  %i17 = sub i32 1075, %i3
  %i18 = zext i32 %i17 to i64
  %.sh9 = shl i64 -1, %i18
  %.neg = freeze i64 %.sh9
  %i19 = and i64 %arg, %.neg
  %i13 = and i64 %arg, 4503599627370495
  %i14 = icmp eq i64 %i13, 0
  %i15 = or i1 %i14, %i12
  %.m5 = sext i1 %i15 to i64
  %.a6 = and i64 %arg, %.m5
  %.n7 = xor i64 %.m5, -1
  %.a8 = and i64 9221120237041090560, %.n7
  %spec.select4 = or i64 %.a6, %.a8
  %.n10 = xor i1 %i10, true
  %.n11 = xor i1 %i4, true
  %.c12 = and i1 %.n10, %.n11
  %.m13 = sext i1 %.c12 to i64
  %.a14 = and i64 %i19, %.m13
  %.m15 = sext i1 %i4 to i64
  %.a16 = and i64 %spec.select, %.m15
  %.o17 = or i64 %.a14, %.a16
  %.m19 = sext i1 %i10 to i64
  %.a20 = and i64 %spec.select4, %.m19
  %.o21 = or i64 %.o17, %.a20
  ret i64 %.o21
}

!llvm.ident = !{!0, !0, !0, !0, !0, !0, !0}
!llvm.module.flags = !{!1, !2, !3, !5}

!0 = !{!"Ubuntu clang version 21.1.8 (6ubuntu1)"}
!1 = !{i32 1, !"wchar_size", i32 4}
!2 = !{i32 1, !"target-abi", !"lp64"}
!3 = distinct !{i32 6, !"riscv-isa", !4}
!4 = distinct !{!"rv64i2p1_m2p0_zmmul1p0"}
!5 = !{i32 8, !"SmallDataLimit", i32 0}
