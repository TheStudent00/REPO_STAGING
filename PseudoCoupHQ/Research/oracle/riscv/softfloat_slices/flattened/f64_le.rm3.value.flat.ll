; ModuleID = '<scratch>/fl/run/f64_le.rm3.value/f64_le.rm3.value.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local zeroext i1 @f64_le_rm3_value_flat(i64 %arg, i64 %arg1) {
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
  %.c5 = and i1 %i5, %i11
  %i13 = xor i64 %arg1, %arg
  %i14 = icmp sgt i64 %i13, -1
  %i16 = icmp slt i64 %arg, 0
  %i17 = and i64 %arg1, 9223372036854775807
  %i18 = or i64 %i17, %arg
  %i19 = icmp eq i64 %i18, 0
  %i20 = or i1 %i16, %i19
  %i22 = icmp eq i64 %arg, %arg1
  %i23 = icmp ult i64 %arg, %arg1
  %i25 = xor i1 %i16, %i23
  %i26 = or i1 %i22, %i25
  %.a3 = and i1 %i26, %i14
  %.n1 = xor i1 %i14, true
  %.a2 = and i1 %i20, %.n1
  %.o4 = or i1 %.a2, %.a3
  %.a6 = and i1 %.o4, %.c5
  ret i1 %.a6
}

!llvm.ident = !{!0, !0, !0, !0, !0, !0}
!llvm.module.flags = !{!1, !2, !3, !5}

!0 = !{!"Ubuntu clang version 21.1.8 (6ubuntu1)"}
!1 = !{i32 1, !"wchar_size", i32 4}
!2 = !{i32 1, !"target-abi", !"lp64"}
!3 = distinct !{i32 6, !"riscv-isa", !4}
!4 = distinct !{!"rv64i2p1_m2p0_zmmul1p0"}
!5 = !{i32 8, !"SmallDataLimit", i32 0}
