; ModuleID = '<scratch>/fl/run/f32_eq.rm2.value/f32_eq.rm2.value.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local zeroext i1 @f32_eq_rm2_value_flat(i64 %arg, i64 %arg1) {
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
  %.c1 = and i1 %i7, %i13
  %i15 = icmp eq i32 %i, %i2
  %i16 = or i32 %i2, %i
  %i17 = and i32 %i16, 2147483647
  %i18 = icmp eq i32 %i17, 0
  %i19 = or i1 %i15, %i18
  %.a2 = and i1 %i19, %.c1
  ret i1 %.a2
}

!llvm.ident = !{!0, !0, !0, !0, !0, !0}
!llvm.module.flags = !{!1, !2, !3, !5}

!0 = !{!"Ubuntu clang version 21.1.8 (6ubuntu1)"}
!1 = !{i32 1, !"wchar_size", i32 4}
!2 = !{i32 1, !"target-abi", !"lp64"}
!3 = distinct !{i32 6, !"riscv-isa", !4}
!4 = distinct !{!"rv64i2p1_m2p0_zmmul1p0"}
!5 = !{i32 8, !"SmallDataLimit", i32 0}
