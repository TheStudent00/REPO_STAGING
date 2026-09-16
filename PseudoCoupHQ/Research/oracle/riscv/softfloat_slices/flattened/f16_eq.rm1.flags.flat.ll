; ModuleID = '<scratch>/fl/run/f16_eq.rm1.flags/f16_eq.rm1.flags.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local i64 @f16_eq_rm1_flags_flat(i64 %arg, i64 %arg1) {
  %i = trunc i64 %arg to i32
  %i2 = trunc i64 %arg1 to i32
  %i3 = and i32 %i, 31744
  %i4 = icmp ne i32 %i3, 31744
  %i5 = and i32 %i, 1023
  %i6 = icmp eq i32 %i5, 0
  %i7 = or i1 %i4, %i6
  %i9 = and i32 %i2, 31744
  %i10 = icmp ne i32 %i9, 31744
  %i11 = and i32 %i2, 1023
  %i12 = icmp eq i32 %i11, 0
  %i13 = or i1 %i10, %i12
  %i15 = and i32 %i, 32256
  %i16 = icmp ne i32 %i15, 31744
  %i17 = and i32 %i, 511
  %i18 = icmp eq i32 %i17, 0
  %i19 = or i1 %i16, %i18
  %i28 = xor i32 %i2, %i
  %i29 = and i32 %i28, 65535
  %i30 = icmp eq i32 %i29, 0
  %i31 = or i32 %i2, %i
  %i32 = and i32 %i31, 32767
  %i33 = icmp eq i32 %i32, 0
  %i34 = or i1 %i30, %i33
  %.m1 = sext i1 %i34 to i64
  %i35 = and i64 256, %.m1
  %i21 = and i32 %i2, 32256
  %i22 = icmp ne i32 %i21, 31744
  %i23 = and i32 %i2, 511
  %i24 = icmp eq i32 %i23, 0
  %i25 = or i1 %i22, %i24
  %.n9 = xor i1 %i25, true
  %.c2 = and i1 %i7, %i13
  %.m3 = sext i1 %.c2 to i64
  %.a4 = and i64 %i35, %.m3
  %.n5 = xor i1 %i13, true
  %.c6 = and i1 %i7, %.n5
  %.n7 = xor i1 %i7, true
  %.c8 = or i1 %.c6, %.n7
  %.c10 = and i1 %.c8, %i19
  %.c11 = and i1 %.c10, %.n9
  %.n12 = xor i1 %i19, true
  %.c13 = and i1 %.c8, %.n12
  %.c14 = or i1 %.c11, %.c13
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
