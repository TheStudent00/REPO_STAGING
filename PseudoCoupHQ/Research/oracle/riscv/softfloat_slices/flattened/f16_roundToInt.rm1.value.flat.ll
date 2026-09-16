; ModuleID = '<scratch>/fl/run/f16_roundToInt.rm1.value/f16_roundToInt.rm1.value.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local i64 @f16_roundToInt_rm1_value_flat(i64 %arg, i1 noundef zeroext %arg1) {
  %i = trunc i64 %arg to i16
  %i2 = trunc i64 %arg to i32
  %i3 = lshr i32 %i2, 10
  %i4 = and i32 %i3, 31
  %i14 = and i32 %i2, 1023
  %i15 = icmp eq i32 %i14, 0
  %i5 = icmp ult i32 %i4, 15
  %i11 = icmp ugt i32 %i4, 24
  %i7 = and i64 %arg, 32767
  %i8 = icmp eq i64 %i7, 0
  %.m1 = sext i1 %i8 to i16
  %i9 = and i16 %i, -32768
  %.a2 = and i16 %i, %.m1
  %.n3 = xor i16 %.m1, -1
  %.a4 = and i16 %i9, %.n3
  %spec.select = or i16 %.a2, %.a4
  %i13 = icmp ne i32 %i4, 31
  %i16 = or i1 %i15, %i13
  %.m5 = sext i1 %i16 to i16
  %i18 = sub i32 25, %i4
  %.sh9 = shl i32 65535, %i18
  %i19 = freeze i32 %.sh9
  %i20 = trunc i32 %i19 to i16
  %i21 = and i16 %i, %i20
  %.a6 = and i16 %i, %.m5
  %.n7 = xor i16 %.m5, -1
  %.a8 = and i16 32256, %.n7
  %spec.select4 = or i16 %.a6, %.a8
  %.n10 = xor i1 %i11, true
  %.n11 = xor i1 %i5, true
  %.c12 = and i1 %.n10, %.n11
  %.m13 = sext i1 %.c12 to i16
  %.a14 = and i16 %i21, %.m13
  %.m15 = sext i1 %i5 to i16
  %.a16 = and i16 %spec.select, %.m15
  %.o17 = or i16 %.a14, %.a16
  %.m19 = sext i1 %i11 to i16
  %.a20 = and i16 %spec.select4, %.m19
  %.o21 = or i16 %.o17, %.a20
  %i23 = zext i16 %.o21 to i64
  ret i64 %i23
}

!llvm.ident = !{!0, !0, !0, !0, !0, !0, !0}
!llvm.module.flags = !{!1, !2, !3, !5}

!0 = !{!"Ubuntu clang version 21.1.8 (6ubuntu1)"}
!1 = !{i32 1, !"wchar_size", i32 4}
!2 = !{i32 1, !"target-abi", !"lp64"}
!3 = distinct !{i32 6, !"riscv-isa", !4}
!4 = distinct !{!"rv64i2p1_m2p0_zmmul1p0"}
!5 = !{i32 8, !"SmallDataLimit", i32 0}
