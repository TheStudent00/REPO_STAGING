; ModuleID = '<scratch>/fl/run/f64_to_ui64.rm2.value/f64_to_ui64.rm2.value.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local i64 @f64_to_ui64_rm2_value_flat(i64 %arg) {
  %i = icmp sgt i64 %arg, -1
  %i1 = lshr i64 %arg, 52
  %i2 = trunc i64 %i1 to i16
  %i3 = and i16 %i2, 2047
  %i4 = and i64 %arg, 4503599627370495
  %i5 = or i64 %i4, 4503599627370496
  %i6 = sub i16 1075, %i3
  %i7 = sext i16 %i6 to i32
  %i18 = icmp ult i16 %i6, 64
  %i8 = icmp ugt i16 %i3, 1074
  %i16 = icmp eq i16 %i3, 0
  %.m1 = sext i1 %i16 to i64
  %.a2 = and i64 %i4, %.m1
  %.n3 = xor i64 %.m1, -1
  %.a4 = and i64 %i5, %.n3
  %i17 = or i64 %.a2, %.a4
  %i25 = icmp ne i64 %i4, 0
  %i10 = icmp ugt i16 %i3, 1086
  %i24 = icmp eq i16 %i3, 2047
  %i26 = and i1 %i25, %i24
  %i27 = or i1 %i26, %i
  %i28 = sext i1 %i27 to i64
  %.m16 = sext i1 %i to i64
  %i20 = zext i32 %i7 to i64
  %.sh5 = lshr i64 %i17, %i20
  %i21 = freeze i64 %.sh5
  %i12 = sub i32 0, %i7
  %i13 = zext i32 %i12 to i64
  %.sh6 = shl i64 %i5, %i13
  %i14 = freeze i64 %.sh6
  %.n7 = xor i1 %i10, true
  %.c8 = and i1 %i8, %.n7
  %.n11 = xor i1 %i8, true
  %.c12 = and i1 %.n11, %i18
  %.m13 = sext i1 %.c12 to i64
  %.a14 = and i64 %i21, %.m13
  %.m18 = sext i1 %i10 to i64
  %.a19 = and i64 %i28, %.m18
  %.m9 = sext i1 %.c8 to i64
  %.a10 = and i64 %i14, %.m9
  %.o15 = or i64 %.a10, %.a14
  %spec.select = and i64 %.o15, %.m16
  %.m21 = sext i1 %.n7 to i64
  %.a22 = and i64 %spec.select, %.m21
  %.o23 = or i64 %.a19, %.a22
  ret i64 %.o23
}

!llvm.ident = !{!0, !0, !0, !0, !0, !0, !0, !0}
!llvm.module.flags = !{!1, !2, !3, !5}

!0 = !{!"Ubuntu clang version 21.1.8 (6ubuntu1)"}
!1 = !{i32 1, !"wchar_size", i32 4}
!2 = !{i32 1, !"target-abi", !"lp64"}
!3 = distinct !{i32 6, !"riscv-isa", !4}
!4 = distinct !{!"rv64i2p1_m2p0_zmmul1p0"}
!5 = !{i32 8, !"SmallDataLimit", i32 0}
