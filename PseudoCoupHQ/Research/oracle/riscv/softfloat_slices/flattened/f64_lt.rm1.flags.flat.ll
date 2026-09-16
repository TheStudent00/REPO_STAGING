; ModuleID = '<scratch>/fl/run/f64_lt.rm1.flags/f64_lt.rm1.flags.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local i64 @f64_lt_rm1_flags_flat(i64 %arg, i64 %arg1) {
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
  %i13 = xor i64 %arg1, %arg
  %i14 = icmp sgt i64 %i13, -1
  %i16 = icmp slt i64 %arg, 0
  %i17 = or i64 %arg1, %arg
  %i18 = and i64 %i17, 9223372036854775807
  %i19 = icmp ne i64 %i18, 0
  %i20 = and i1 %i16, %i19
  %i22 = icmp ne i64 %arg, %arg1
  %i23 = icmp ult i64 %arg, %arg1
  %i25 = xor i1 %i16, %i23
  %i26 = and i1 %i22, %i25
  %.a9 = and i1 %i26, %i14
  %.n10 = xor i1 %i14, true
  %.a11 = and i1 %i20, %.n10
  %.o12 = or i1 %.a9, %.a11
  %.n1 = xor i1 %i11, true
  %.c2 = and i1 %i5, %.n1
  %.m3 = sext i1 %.c2 to i64
  %.a4 = and i64 16, %.m3
  %.c13 = and i1 %i5, %i11
  %.a14 = and i1 %.o12, %.c13
  %.n5 = xor i1 %i5, true
  %.m6 = sext i1 %.n5 to i64
  %.a7 = and i64 16, %.m6
  %.o8 = or i64 %.a4, %.a7
  %.m15 = sext i1 %.a14 to i64
  %i28 = and i64 256, %.m15
  %i29 = or i64 %i28, %.o8
  ret i64 %i29
}

!llvm.ident = !{!0, !0, !0, !0, !0, !0}
!llvm.module.flags = !{!1, !2, !3, !5}

!0 = !{!"Ubuntu clang version 21.1.8 (6ubuntu1)"}
!1 = !{i32 1, !"wchar_size", i32 4}
!2 = !{i32 1, !"target-abi", !"lp64"}
!3 = distinct !{i32 6, !"riscv-isa", !4}
!4 = distinct !{!"rv64i2p1_m2p0_zmmul1p0"}
!5 = !{i32 8, !"SmallDataLimit", i32 0}
