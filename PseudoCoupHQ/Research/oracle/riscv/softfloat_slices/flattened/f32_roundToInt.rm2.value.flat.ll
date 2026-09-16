; ModuleID = '<scratch>/fl/run/f32_roundToInt.rm2.value/f32_roundToInt.rm2.value.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local i64 @f32_roundToInt_rm2_value_flat(i64 %arg, i1 noundef zeroext %arg1) {
  %i = trunc i64 %arg to i32
  %i2 = lshr i32 %i, 23
  %i3 = and i32 %i2, 255
  %i4 = icmp ult i32 %i3, 127
  %i11 = icmp ugt i32 %i3, 149
  %i6 = and i32 %i, 2147483647
  %i7 = icmp eq i32 %i6, 0
  %i13 = icmp ne i32 %i3, 255
  %i18 = sub i32 150, %i3
  %.sh5 = shl i32 1, %i18
  %i19 = freeze i32 %.sh5
  %i14 = and i32 %i, 8388607
  %i15 = icmp eq i32 %i14, 0
  %i16 = or i1 %i15, %i13
  %.m1 = sext i1 %i16 to i32
  %.a2 = and i32 %i, %.m1
  %.n3 = xor i32 %.m1, -1
  %.a4 = and i32 2143289344, %.n3
  %spec.select = or i32 %.a2, %.a4
  %i20 = add i32 %i19, -1
  %i24 = sub i32 0, %i19
  %i21 = icmp slt i32 %i, 0
  %.m6 = sext i1 %i21 to i32
  %i22 = and i32 %i20, %.m6
  %i23 = add i32 %i22, %i
  %i25 = and i32 %i23, %i24
  %i9 = and i32 -1082130432, %.m6
  %.c8 = and i1 %i7, %i4
  %.m9 = sext i1 %.c8 to i32
  %.a10 = and i32 %i, %.m9
  %.n11 = xor i1 %i7, true
  %.c12 = and i1 %.n11, %i4
  %.m13 = sext i1 %.c12 to i32
  %.a14 = and i32 %i9, %.m13
  %.o15 = or i32 %.a10, %.a14
  %.n17 = xor i1 %i4, true
  %.n16 = xor i1 %i11, true
  %.c18 = and i1 %.n16, %.n17
  %.m19 = sext i1 %.c18 to i32
  %.a20 = and i32 %i25, %.m19
  %.o21 = or i32 %.o15, %.a20
  %.m23 = sext i1 %i11 to i32
  %.a24 = and i32 %spec.select, %.m23
  %.o25 = or i32 %.o21, %.a24
  %i27 = zext i32 %.o25 to i64
  ret i64 %i27
}

!llvm.ident = !{!0, !0, !0, !0, !0, !0, !0}
!llvm.module.flags = !{!1, !2, !3, !5}

!0 = !{!"Ubuntu clang version 21.1.8 (6ubuntu1)"}
!1 = !{i32 1, !"wchar_size", i32 4}
!2 = !{i32 1, !"target-abi", !"lp64"}
!3 = distinct !{i32 6, !"riscv-isa", !4}
!4 = distinct !{!"rv64i2p1_m2p0_zmmul1p0"}
!5 = !{i32 8, !"SmallDataLimit", i32 0}
