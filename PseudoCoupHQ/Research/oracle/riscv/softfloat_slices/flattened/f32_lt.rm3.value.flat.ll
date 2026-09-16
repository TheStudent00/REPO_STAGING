; ModuleID = '<scratch>/fl/run/f32_lt.rm3.value/f32_lt.rm3.value.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local zeroext i1 @f32_lt_rm3_value_flat(i64 %arg, i64 %arg1) {
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
  %.c5 = and i1 %i7, %i13
  %i15 = xor i32 %i2, %i
  %i16 = icmp sgt i32 %i15, -1
  %i18 = icmp slt i32 %i, 0
  %i19 = or i32 %i2, %i
  %i20 = and i32 %i19, 2147483647
  %i21 = icmp ne i32 %i20, 0
  %i22 = and i1 %i18, %i21
  %i24 = icmp ne i32 %i, %i2
  %i25 = icmp ult i32 %i, %i2
  %i27 = xor i1 %i18, %i25
  %i28 = and i1 %i24, %i27
  %.a3 = and i1 %i28, %i16
  %.n1 = xor i1 %i16, true
  %.a2 = and i1 %i22, %.n1
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
