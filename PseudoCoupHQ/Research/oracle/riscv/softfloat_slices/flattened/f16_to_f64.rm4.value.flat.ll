; ModuleID = '<scratch>/fl/run/f16_to_f64.rm4.value/f16_to_f64.rm4.value.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local i64 @f16_to_f64_rm4_value_flat(i64 %arg) {
  %i = and i64 %arg, 32768
  %.not.not = icmp eq i64 %i, 0
  %.sh11 = shl i64 %i, 48
  %i12 = freeze i64 %.sh11
  %i1 = lshr i64 %arg, 10
  %i2 = trunc i64 %i1 to i8
  %i3 = and i8 %i2, 31
  %i4 = trunc i64 %arg to i16
  %i5 = and i16 %i4, 1023
  %.q1 = icmp eq i8 %i3, 31
  %.q2 = icmp eq i8 %i3, 0
  %i7 = icmp eq i16 %i5, 0
  %.m7 = sext i1 %i7 to i64
  %.m3 = sext i1 %.not.not to i64
  %.a4 = and i64 9218868437227405312, %.m3
  %.n5 = xor i64 %.m3, -1
  %.a6 = and i64 -4503599627370496, %.n5
  %i8 = or i64 %.a4, %.a6
  %.a8 = and i64 %i8, %.m7
  %.n9 = xor i64 %.m7, -1
  %.a10 = and i64 9221120237041090560, %.n9
  %spec.select = or i64 %.a8, %.a10
  %i14 = zext i16 %i5 to i32
  %.k12 = call range(i32 16, 33) i32 @llvm.ctlz.i32(i32 %i14, i1 true)
  %i15 = freeze i32 %.k12
  %i16 = add i32 %i15, 235
  %i17 = and i32 %i16, 255
  %.sh13 = shl i32 %i14, %i17
  %i18 = freeze i32 %.sh13
  %i19 = trunc i32 %i15 to i8
  %i20 = trunc i32 %i18 to i16
  %i21 = sub i8 21, %i19
  %.n14 = xor i1 %i7, true
  %.c15 = and i1 %.q2, %.n14
  %.c37 = and i1 %.q2, %i7
  %.c18 = or i1 %.q2, %.q1
  %.n19 = xor i1 %.c18, true
  %.m38 = sext i1 %.c37 to i64
  %.a39 = and i64 %i12, %.m38
  %.m41 = sext i1 %.q1 to i64
  %.a42 = and i64 %spec.select, %.m41
  %.m16 = sext i1 %.c15 to i16
  %.a17 = and i16 %i20, %.m16
  %.m20 = sext i1 %.n19 to i16
  %.a21 = and i16 %i5, %.m20
  %.o22 = or i16 %.a17, %.a21
  %i27 = zext i16 %.o22 to i64
  %.sh29 = shl i64 %i27, 42
  %i28 = freeze i64 %.sh29
  %.m23 = sext i1 %.c15 to i8
  %.a24 = and i8 %i21, %.m23
  %.c34 = or i1 %.c15, %.n19
  %.m25 = sext i1 %.n19 to i8
  %.a26 = and i8 %i3, %.m25
  %.o27 = or i8 %.a24, %.a26
  %i25 = sext i8 %.o27 to i64
  %.sh28 = shl i64 %i25, 52
  %i26 = freeze i64 %.sh28
  %.m35 = sext i1 %.c34 to i64
  %.a31 = and i64 4539628424389459968, %.m3
  %.a33 = and i64 -4683743612465315840, %.n5
  %i29 = or i64 %.a31, %.a33
  %i30 = add i64 %i29, %i28
  %i31 = add i64 %i30, %i26
  %.a36 = and i64 %i31, %.m35
  %.o40 = or i64 %.a36, %.a39
  %.o43 = or i64 %.o40, %.a42
  ret i64 %.o43
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
