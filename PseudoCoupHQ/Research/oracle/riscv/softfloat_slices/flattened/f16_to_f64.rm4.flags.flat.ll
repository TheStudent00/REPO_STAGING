; ModuleID = '<scratch>/fl/run/f16_to_f64.rm4.flags/f16_to_f64.rm4.flags.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local [2 x i64] @f16_to_f64_rm4_flags_flat(i64 %arg) {
  %i = and i64 %arg, 32768
  %.not.not = icmp eq i64 %i, 0
  %.sh3 = shl i64 %i, 48
  %i16 = freeze i64 %.sh3
  %i1 = lshr i64 %arg, 10
  %i2 = trunc i64 %i1 to i8
  %i3 = and i8 %i2, 31
  %i4 = trunc i64 %arg to i16
  %i5 = and i16 %i4, 1023
  %.q1 = icmp eq i8 %i3, 31
  %.q2 = icmp eq i8 %i3, 0
  %i14 = icmp eq i16 %i5, 0
  %i18 = zext i16 %i5 to i32
  %.k4 = call range(i32 16, 33) i32 @llvm.ctlz.i32(i32 %i18, i1 true)
  %i19 = freeze i32 %.k4
  %i20 = add i32 %i19, 235
  %i21 = and i32 %i20, 255
  %.sh5 = shl i32 %i18, %i21
  %i22 = freeze i32 %.sh5
  %i23 = trunc i32 %i19 to i8
  %i24 = trunc i32 %i22 to i16
  %i25 = sub i8 21, %i23
  %.m6 = sext i1 %.not.not to i64
  %.a7 = and i64 9218868437227405312, %.m6
  %.n8 = xor i64 %.m6, -1
  %.a9 = and i64 -4503599627370496, %.n8
  %i12 = or i64 %.a7, %.a9
  %i9 = and i64 %arg, 512
  %i10 = icmp eq i64 %i9, 0
  %.m10 = sext i1 %i10 to i64
  %spec.select = and i64 16, %.m10
  %.n11 = xor i1 %i14, true
  %.c12 = and i1 %.q2, %.n11
  %.c42 = and i1 %.q2, %i14
  %.c15 = or i1 %.q1, %.q2
  %.n16 = xor i1 %.c15, true
  %.m43 = sext i1 %.c42 to i64
  %.a44 = and i64 %i16, %.m43
  %.m13 = sext i1 %.c12 to i16
  %.a14 = and i16 %i24, %.m13
  %.m17 = sext i1 %.n16 to i16
  %.a18 = and i16 %i5, %.m17
  %.o19 = or i16 %.a14, %.a18
  %i31 = zext i16 %.o19 to i64
  %.sh26 = shl i64 %i31, 42
  %i32 = freeze i64 %.sh26
  %.m20 = sext i1 %.c12 to i8
  %.a21 = and i8 %i25, %.m20
  %.c35 = or i1 %.c12, %.n16
  %.m22 = sext i1 %.n16 to i8
  %.a23 = and i8 %i3, %.m22
  %.o24 = or i8 %.a21, %.a23
  %i29 = sext i8 %.o24 to i64
  %.sh25 = shl i64 %i29, 52
  %i30 = freeze i64 %.sh25
  %.m36 = sext i1 %.c35 to i64
  %.a28 = and i64 4539628424389459968, %.m6
  %.a30 = and i64 -4683743612465315840, %.n8
  %i33 = or i64 %.a28, %.a30
  %i34 = add i64 %i33, %i32
  %i35 = add i64 %i34, %i30
  %.a37 = and i64 %i35, %.m36
  %.c32 = and i1 %.n11, %.q1
  %.c38 = and i1 %i14, %.q1
  %.m33 = sext i1 %.c32 to i64
  %.a34 = and i64 %spec.select, %.m33
  %.m39 = sext i1 %.c38 to i64
  %.a40 = and i64 %i12, %.m39
  %.o41 = or i64 %.a37, %.a40
  %.o45 = or i64 %.o41, %.a44
  %.a46 = and i64 9221120237041090560, %.m33
  %.o47 = or i64 %.o45, %.a46
  %i37 = insertvalue [2 x i64] poison, i64 %.a34, 0
  %i38 = insertvalue [2 x i64] %i37, i64 %.o47, 1
  ret [2 x i64] %i38
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
