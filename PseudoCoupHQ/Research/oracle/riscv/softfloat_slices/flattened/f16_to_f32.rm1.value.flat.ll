; ModuleID = '<scratch>/fl/run/f16_to_f32.rm1.value/f16_to_f32.rm1.value.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local i64 @f16_to_f32_rm1_value_flat(i64 %arg) {
  %i = trunc i64 %arg to i32
  %i1 = and i32 %i, 32768
  %i2 = icmp eq i32 %i1, 0
  %.m3 = sext i1 %i2 to i32
  %i3 = lshr i64 %arg, 10
  %i4 = trunc i64 %i3 to i8
  %i5 = and i8 %i4, 31
  %i6 = trunc i64 %arg to i16
  %i7 = and i16 %i6, 1023
  %.q1 = icmp eq i8 %i5, 31
  %.q2 = icmp eq i8 %i5, 0
  %i12 = icmp eq i16 %i7, 0
  %.m7 = sext i1 %i12 to i32
  %.a4 = and i32 2139095040, %.m3
  %.n5 = xor i32 %.m3, -1
  %.a6 = and i32 -8388608, %.n5
  %i10 = or i32 %.a4, %.a6
  %.a8 = and i32 %i10, %.m7
  %.n9 = xor i32 %.m7, -1
  %.a10 = and i32 2143289344, %.n9
  %spec.select = or i32 %.a8, %.a10
  %.sh11 = shl i32 %i1, 16
  %i14 = freeze i32 %.sh11
  %i32 = or i32 %i14, 939524096
  %i16 = zext i16 %i7 to i32
  %.k12 = call range(i32 16, 33) i32 @llvm.ctlz.i32(i32 %i16, i1 true)
  %i17 = freeze i32 %.k12
  %i18 = add i32 %i17, 235
  %i19 = and i32 %i18, 255
  %.sh13 = shl i32 %i16, %i19
  %i20 = freeze i32 %.sh13
  %i21 = trunc i32 %i17 to i8
  %i22 = trunc i32 %i20 to i16
  %i23 = sub i8 21, %i21
  %.n14 = xor i1 %i12, true
  %.c15 = and i1 %.q2, %.n14
  %.c34 = and i1 %.q2, %i12
  %.c18 = or i1 %.q1, %.q2
  %.n19 = xor i1 %.c18, true
  %.m35 = sext i1 %.c34 to i32
  %.a36 = and i32 %i14, %.m35
  %.m38 = sext i1 %.q1 to i32
  %.a39 = and i32 %spec.select, %.m38
  %.m16 = sext i1 %.c15 to i16
  %.a17 = and i16 %i22, %.m16
  %.m20 = sext i1 %.n19 to i16
  %.a21 = and i16 %i7, %.m20
  %.o22 = or i16 %.a17, %.a21
  %i30 = zext i16 %.o22 to i32
  %.sh30 = shl i32 %i30, 13
  %i31 = freeze i32 %.sh30
  %i33 = add i32 %i32, %i31
  %.m23 = sext i1 %.c15 to i8
  %.a24 = and i8 %i23, %.m23
  %.c31 = or i1 %.c15, %.n19
  %.m25 = sext i1 %.n19 to i8
  %.a26 = and i8 %i5, %.m25
  %.o27 = or i8 %.a24, %.a26
  %i28 = sext i8 %.o27 to i32
  %.sh29 = shl i32 %i28, 23
  %i29 = freeze i32 %.sh29
  %i34 = add i32 %i33, %i29
  %.m32 = sext i1 %.c31 to i32
  %.a33 = and i32 %i34, %.m32
  %.o37 = or i32 %.a33, %.a36
  %.o40 = or i32 %.o37, %.a39
  %i36 = zext i32 %.o40 to i64
  ret i64 %i36
}

; Function Attrs: nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare i32 @llvm.ctlz.i32(i32, i1 immarg) #0

attributes #0 = { nocallback nofree nosync nounwind speculatable willreturn memory(none) }

!llvm.ident = !{!0, !0, !0, !0, !0, !0, !0}
!llvm.module.flags = !{!1, !2, !3, !5}

!0 = !{!"Ubuntu clang version 21.1.8 (6ubuntu1)"}
!1 = !{i32 1, !"wchar_size", i32 4}
!2 = !{i32 1, !"target-abi", !"lp64"}
!3 = distinct !{i32 6, !"riscv-isa", !4}
!4 = distinct !{!"rv64i2p1_m2p0_zmmul1p0"}
!5 = !{i32 8, !"SmallDataLimit", i32 0}
