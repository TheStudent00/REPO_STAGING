; ModuleID = '<scratch>/fl/run/f32_roundToInt.rm1.value/f32_roundToInt.rm1.value.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local i64 @f32_roundToInt_rm1_value_flat(i64 %arg, i1 noundef zeroext %arg1) {
  %i = trunc i64 %arg to i32
  %i2 = lshr i32 %i, 23
  %i3 = and i32 %i2, 255
  %i4 = icmp ult i32 %i3, 127
  %i6 = and i32 %i, 2147483647
  %i7 = icmp eq i32 %i6, 0
  %.m1 = sext i1 %i7 to i32
  %i8 = and i32 %i, -2147483648
  %.a2 = and i32 %i, %.m1
  %.n3 = xor i32 %.m1, -1
  %.a4 = and i32 %i8, %.n3
  %spec.select = or i32 %.a2, %.a4
  %i10 = icmp ugt i32 %i3, 149
  %i12 = icmp ne i32 %i3, 255
  %i17 = sub i32 150, %i3
  %.sh9 = shl i32 -1, %i17
  %.neg = freeze i32 %.sh9
  %i18 = and i32 %.neg, %i
  %i13 = and i32 %i, 8388607
  %i14 = icmp eq i32 %i13, 0
  %i15 = or i1 %i14, %i12
  %.m5 = sext i1 %i15 to i32
  %.a6 = and i32 %i, %.m5
  %.n7 = xor i32 %.m5, -1
  %.a8 = and i32 2143289344, %.n7
  %spec.select4 = or i32 %.a6, %.a8
  %.n10 = xor i1 %i10, true
  %.n11 = xor i1 %i4, true
  %.c12 = and i1 %.n10, %.n11
  %.m13 = sext i1 %.c12 to i32
  %.a14 = and i32 %i18, %.m13
  %.m15 = sext i1 %i4 to i32
  %.a16 = and i32 %spec.select, %.m15
  %.o17 = or i32 %.a14, %.a16
  %.m19 = sext i1 %i10 to i32
  %.a20 = and i32 %spec.select4, %.m19
  %.o21 = or i32 %.o17, %.a20
  %i20 = zext i32 %.o21 to i64
  ret i64 %i20
}

!llvm.ident = !{!0, !0, !0, !0, !0, !0, !0}
!llvm.module.flags = !{!1, !2, !3, !5}

!0 = !{!"Ubuntu clang version 21.1.8 (6ubuntu1)"}
!1 = !{i32 1, !"wchar_size", i32 4}
!2 = !{i32 1, !"target-abi", !"lp64"}
!3 = distinct !{i32 6, !"riscv-isa", !4}
!4 = distinct !{!"rv64i2p1_m2p0_zmmul1p0"}
!5 = !{i32 8, !"SmallDataLimit", i32 0}
