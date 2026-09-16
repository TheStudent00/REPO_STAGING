; ModuleID = '<scratch>/fl/run/f16_lt.rm1.value/f16_lt.rm1.value.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local zeroext i1 @f16_lt_rm1_value_flat(i64 %arg, i64 %arg1) {
  %i = trunc i64 %arg to i32
  %i2 = and i32 %i, 65535
  %i3 = trunc i64 %arg1 to i32
  %i4 = and i32 %i3, 65535
  %i5 = and i32 %i, 31744
  %i6 = icmp ne i32 %i5, 31744
  %i7 = and i32 %i, 1023
  %i8 = icmp eq i32 %i7, 0
  %i9 = or i1 %i6, %i8
  %i21 = or i32 %i3, %i
  %i22 = and i32 %i21, 32767
  %i23 = icmp ne i32 %i22, 0
  %i11 = and i32 %i3, 31744
  %i12 = icmp ne i32 %i11, 31744
  %i13 = and i32 %i3, 1023
  %i14 = icmp eq i32 %i13, 0
  %i15 = or i1 %i12, %i14
  %.c5 = and i1 %i9, %i15
  %i17 = icmp ugt i32 %i2, 32767
  %i24 = and i1 %i17, %i23
  %i18 = icmp ult i32 %i4, 32768
  %i19 = xor i1 %i17, %i18
  %i26 = icmp ne i32 %i2, %i4
  %i27 = icmp ult i32 %i2, %i4
  %i28 = xor i1 %i17, %i27
  %i29 = and i1 %i26, %i28
  %.a3 = and i1 %i29, %i19
  %.n1 = xor i1 %i19, true
  %.a2 = and i1 %i24, %.n1
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
