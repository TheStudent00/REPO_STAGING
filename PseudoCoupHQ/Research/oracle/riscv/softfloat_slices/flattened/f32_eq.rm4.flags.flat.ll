; ModuleID = '<scratch>/fl/run/f32_eq.rm4.flags/f32_eq.rm4.flags.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local i64 @f32_eq_rm4_flags_flat(i64 %arg, i64 %arg1) {
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
  %i15 = and i32 %i, 2143289344
  %i16 = icmp ne i32 %i15, 2139095040
  %i17 = and i32 %i, 4194303
  %i18 = icmp eq i32 %i17, 0
  %i19 = or i1 %i16, %i18
  %i28 = icmp eq i32 %i, %i2
  %i29 = or i32 %i2, %i
  %i30 = and i32 %i29, 2147483647
  %i31 = icmp eq i32 %i30, 0
  %i32 = or i1 %i28, %i31
  %.m1 = sext i1 %i32 to i64
  %i33 = and i64 256, %.m1
  %i21 = and i32 %i2, 2143289344
  %i22 = icmp ne i32 %i21, 2139095040
  %i23 = and i32 %i2, 4194303
  %i24 = icmp eq i32 %i23, 0
  %i25 = or i1 %i22, %i24
  %.n11 = xor i1 %i25, true
  %.c2 = and i1 %i7, %i13
  %.m3 = sext i1 %.c2 to i64
  %.a4 = and i64 %i33, %.m3
  %.n6 = xor i1 %i13, true
  %.c7 = and i1 %i7, %.n6
  %.n5 = xor i1 %i7, true
  %.c8 = or i1 %.n5, %.c7
  %.n9 = xor i1 %i19, true
  %.c10 = and i1 %.c8, %.n9
  %.c12 = and i1 %.c8, %i19
  %.c13 = and i1 %.c12, %.n11
  %.c14 = or i1 %.c10, %.c13
  %.m15 = sext i1 %.c14 to i64
  %.a16 = and i64 16, %.m15
  %.o17 = or i64 %.a4, %.a16
  ret i64 %.o17
}

!llvm.ident = !{!0, !0, !0, !0, !0, !0}
!llvm.module.flags = !{!1, !2, !3, !5}

!0 = !{!"Ubuntu clang version 21.1.8 (6ubuntu1)"}
!1 = !{i32 1, !"wchar_size", i32 4}
!2 = !{i32 1, !"target-abi", !"lp64"}
!3 = distinct !{i32 6, !"riscv-isa", !4}
!4 = distinct !{!"rv64i2p1_m2p0_zmmul1p0"}
!5 = !{i32 8, !"SmallDataLimit", i32 0}
