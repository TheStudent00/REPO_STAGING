; ModuleID = '<scratch>/fl/run/f32_to_ui64.rm2.value/f32_to_ui64.rm2.value.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local i64 @f32_to_ui64_rm2_value_flat(i64 %arg) {
  %i = trunc i64 %arg to i32
  %i1 = icmp sgt i32 %i, -1
  %i2 = lshr i32 %i, 23
  %i4 = and i32 %i2, 255
  %i3 = and i32 %i, 8388607
  %i14 = and i32 %i, 2139095040
  %i15 = icmp eq i32 %i14, 0
  %.m1 = sext i1 %i15 to i32
  %i5 = sub i32 190, %i4
  %i6 = icmp ugt i32 %i4, 190
  %i16 = or i32 %i3, 8388608
  %.a2 = and i32 %i3, %.m1
  %.n3 = xor i32 %.m1, -1
  %.a4 = and i32 %i16, %.n3
  %i17 = or i32 %.a2, %.a4
  %i18 = zext i32 %i17 to i64
  %.sh5 = shl i64 %i18, 40
  %i19 = freeze i64 %.sh5
  %i9 = icmp ne i32 %i3, 0
  %i20 = icmp eq i32 %i4, 190
  %i8 = icmp eq i32 %i4, 255
  %i10 = and i1 %i9, %i8
  %i11 = or i1 %i10, %i1
  %i12 = sext i1 %i11 to i64
  %.m17 = sext i1 %i1 to i64
  %i22 = icmp ult i32 %i5, 64
  %i24 = zext i32 %i5 to i64
  %.sh6 = lshr i64 %i19, %i24
  %i25 = freeze i64 %.sh6
  %.m7 = sext i1 %i20 to i64
  %.a8 = and i64 %i19, %.m7
  %.n9 = xor i1 %i20, true
  %.c10 = and i1 %.n9, %i22
  %.m11 = sext i1 %.c10 to i64
  %.a12 = and i64 %i25, %.m11
  %.o13 = or i64 %.a8, %.a12
  %.n14 = xor i1 %i6, true
  %.m15 = sext i1 %.n14 to i64
  %.a16 = and i64 %.o13, %.m15
  %spec.select = and i64 %.a16, %.m17
  %.m18 = sext i1 %i6 to i64
  %.a19 = and i64 %i12, %.m18
  %.o21 = or i64 %.a19, %spec.select
  ret i64 %.o21
}

!llvm.ident = !{!0, !0, !0, !0, !0, !0, !0, !0}
!llvm.module.flags = !{!1, !2, !3, !5}

!0 = !{!"Ubuntu clang version 21.1.8 (6ubuntu1)"}
!1 = !{i32 1, !"wchar_size", i32 4}
!2 = !{i32 1, !"target-abi", !"lp64"}
!3 = distinct !{i32 6, !"riscv-isa", !4}
!4 = distinct !{!"rv64i2p1_m2p0_zmmul1p0"}
!5 = !{i32 8, !"SmallDataLimit", i32 0}
