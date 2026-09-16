; ModuleID = '<scratch>/fl/run/f32_le.rm3.flags/f32_le.rm3.flags.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local i64 @f32_le_rm3_flags_flat(i64 %arg, i64 %arg1) {
  %i = trunc i64 %arg to i32
  %i2 = trunc i64 %arg1 to i32
  %i3 = and i32 %i, 2139095040
  %i4 = icmp ne i32 %i3, 2139095040
  %i5 = and i32 %i, 8388607
  %i6 = icmp eq i32 %i5, 0
  %i7 = or i1 %i4, %i6
  %i9 = and i32 %i2, 2139095040
  %i10 = icmp ne i32 %i9, 2139095040
  %i11 = and i32 %i2, 8388607
  %i12 = icmp eq i32 %i11, 0
  %i13 = or i1 %i10, %i12
  %i15 = xor i32 %i2, %i
  %i16 = icmp sgt i32 %i15, -1
  %i18 = icmp slt i32 %i, 0
  %i19 = and i32 %i2, 2147483647
  %i20 = or i32 %i19, %i
  %i21 = icmp eq i32 %i20, 0
  %i22 = or i1 %i18, %i21
  %i24 = icmp eq i32 %i, %i2
  %i25 = icmp ult i32 %i, %i2
  %i27 = xor i1 %i18, %i25
  %i28 = or i1 %i24, %i27
  %.a9 = and i1 %i28, %i16
  %.n10 = xor i1 %i16, true
  %.a11 = and i1 %i22, %.n10
  %.o12 = or i1 %.a9, %.a11
  %.n1 = xor i1 %i13, true
  %.c2 = and i1 %i7, %.n1
  %.m3 = sext i1 %.c2 to i64
  %.a4 = and i64 16, %.m3
  %.c13 = and i1 %i7, %i13
  %.a14 = and i1 %.o12, %.c13
  %.n5 = xor i1 %i7, true
  %.m6 = sext i1 %.n5 to i64
  %.a7 = and i64 16, %.m6
  %.o8 = or i64 %.a4, %.a7
  %.m15 = sext i1 %.a14 to i64
  %i30 = and i64 256, %.m15
  %i31 = or i64 %i30, %.o8
  ret i64 %i31
}

!llvm.ident = !{!0, !0, !0, !0, !0, !0}
!llvm.module.flags = !{!1, !2, !3, !5}

!0 = !{!"Ubuntu clang version 21.1.8 (6ubuntu1)"}
!1 = !{i32 1, !"wchar_size", i32 4}
!2 = !{i32 1, !"target-abi", !"lp64"}
!3 = distinct !{i32 6, !"riscv-isa", !4}
!4 = distinct !{!"rv64i2p1_m2p0_zmmul1p0"}
!5 = !{i32 8, !"SmallDataLimit", i32 0}
