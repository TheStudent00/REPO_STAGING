; ModuleID = '<scratch>/fl/run/f64_eq.rm1.flags/f64_eq.rm1.flags.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local i64 @f64_eq_rm1_flags_flat(i64 %arg, i64 %arg1) {
  %i = and i64 %arg, 9218868437227405312
  %i2 = icmp ne i64 %i, 9218868437227405312
  %i3 = and i64 %arg, 4503599627370495
  %i4 = icmp eq i64 %i3, 0
  %i5 = or i1 %i2, %i4
  %i7 = and i64 %arg1, 9218868437227405312
  %i8 = icmp ne i64 %i7, 9218868437227405312
  %i9 = and i64 %arg1, 4503599627370495
  %i10 = icmp eq i64 %i9, 0
  %i11 = or i1 %i8, %i10
  %i13 = and i64 %arg, 9221120237041090560
  %i14 = icmp ne i64 %i13, 9218868437227405312
  %i15 = and i64 %arg, 2251799813685247
  %i16 = icmp eq i64 %i15, 0
  %i17 = or i1 %i14, %i16
  %i26 = icmp eq i64 %arg, %arg1
  %i27 = or i64 %arg1, %arg
  %i28 = and i64 %i27, 9223372036854775807
  %i29 = icmp eq i64 %i28, 0
  %i30 = or i1 %i26, %i29
  %.m1 = sext i1 %i30 to i64
  %i31 = and i64 256, %.m1
  %i19 = and i64 %arg1, 9221120237041090560
  %i20 = icmp ne i64 %i19, 9218868437227405312
  %i21 = and i64 %arg1, 2251799813685247
  %i22 = icmp eq i64 %i21, 0
  %i23 = or i1 %i20, %i22
  %.n9 = xor i1 %i23, true
  %.c2 = and i1 %i5, %i11
  %.m3 = sext i1 %.c2 to i64
  %.a4 = and i64 %i31, %.m3
  %.n5 = xor i1 %i11, true
  %.c6 = and i1 %i5, %.n5
  %.n7 = xor i1 %i5, true
  %.c8 = or i1 %.c6, %.n7
  %.c10 = and i1 %.c8, %i17
  %.c11 = and i1 %.c10, %.n9
  %.n12 = xor i1 %i17, true
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
