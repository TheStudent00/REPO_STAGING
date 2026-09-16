; ModuleID = '<scratch>/fl/run/f32_roundToInt.rm4.value/f32_roundToInt.rm4.value.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local i64 @f32_roundToInt_rm4_value_flat(i64 %arg, i1 noundef zeroext %arg1) {
  %i = trunc i64 %arg to i32
  %i2 = lshr i32 %i, 23
  %i3 = and i32 %i2, 255
  %i4 = icmp ult i32 %i3, 127
  %i13 = icmp ugt i32 %i3, 149
  %i6 = and i32 %i, 2147483647
  %i7 = icmp eq i32 %i6, 0
  %i15 = icmp ne i32 %i3, 255
  %i16 = and i32 %i, 8388607
  %i17 = icmp eq i32 %i16, 0
  %i18 = or i1 %i17, %i15
  %.m1 = sext i1 %i18 to i32
  %.a2 = and i32 %i, %.m1
  %.n3 = xor i32 %.m1, -1
  %.a4 = and i32 2143289344, %.n3
  %spec.select4 = or i32 %.a2, %.a4
  %i20 = sub i32 150, %i3
  %.sh5 = shl i32 1, %i20
  %i21 = freeze i32 %.sh5
  %i10 = icmp eq i32 %i3, 126
  %.m7 = sext i1 %i10 to i32
  %.sh6 = lshr i32 %i21, 1
  %i23 = add i32 %.sh6, %i
  %i24 = sub i32 0, %i21
  %i25 = and i32 %i23, %i24
  %i9 = and i32 %i, -2147483648
  %i11 = or i32 %i9, 1065353216
  %.a8 = and i32 %i11, %.m7
  %.n9 = xor i32 %.m7, -1
  %.a10 = and i32 %i9, %.n9
  %spec.select = or i32 %.a8, %.a10
  %.c11 = and i1 %i7, %i4
  %.m12 = sext i1 %.c11 to i32
  %.a13 = and i32 %i, %.m12
  %.n14 = xor i1 %i7, true
  %.c15 = and i1 %.n14, %i4
  %.m16 = sext i1 %.c15 to i32
  %.a17 = and i32 %spec.select, %.m16
  %.o18 = or i32 %.a13, %.a17
  %.n19 = xor i1 %i4, true
  %.n20 = xor i1 %i13, true
  %.c21 = and i1 %.n19, %.n20
  %.m22 = sext i1 %.c21 to i32
  %.a23 = and i32 %i25, %.m22
  %.o24 = or i32 %.o18, %.a23
  %.m26 = sext i1 %i13 to i32
  %.a27 = and i32 %spec.select4, %.m26
  %.o28 = or i32 %.o24, %.a27
  %i27 = zext i32 %.o28 to i64
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
