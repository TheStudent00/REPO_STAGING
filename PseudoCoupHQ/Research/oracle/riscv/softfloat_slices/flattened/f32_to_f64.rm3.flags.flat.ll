; ModuleID = '<scratch>/fl/run/f32_to_f64.rm3.flags/f32_to_f64.rm3.flags.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local [2 x i64] @f32_to_f64_rm3_flags_flat(i64 %arg) {
  %i = and i64 %arg, 4294967295
  %i1 = trunc i64 %arg to i32
  %i2 = and i32 %i1, 8388607
  %i3 = and i32 %i1, 2139095040
  %i4 = icmp eq i32 %i3, 2139095040
  %.sh1 = lshr i32 %i1, 23
  %i15 = freeze i32 %.sh1
  %i16 = trunc i32 %i15 to i16
  %i17 = and i16 %i16, 255
  %i8 = and i32 %i1, 4194304
  %i9 = icmp eq i32 %i8, 0
  %.m3 = sext i1 %i9 to i64
  %spec.select = and i64 16, %.m3
  %i18 = icmp eq i16 %i17, 0
  %i6 = icmp eq i32 %i2, 0
  %.sh2 = shl i64 %i, 32
  %i11 = freeze i64 %.sh2
  %i12 = and i64 %i11, -9223372036854775808
  %i13 = or i64 %i12, 9218868437227405312
  %i40 = or i64 %i12, 4035225266123964416
  %.k5 = call range(i32 0, 33) i32 @llvm.ctlz.i32(i32 range(i32 1, 8388608) %i2, i1 true)
  %i25 = freeze i32 %.k5
  %i26 = trunc i32 %i25 to i8
  %i27 = add i32 %i25, 248
  %i28 = and i32 %i27, 255
  %.sh6 = shl i32 %i2, %i28
  %i29 = freeze i32 %.sh6
  %narrow = sub i8 8, %i26
  %i30 = sext i8 %narrow to i16
  %.n7 = xor i1 %i18, true
  %.m8 = sext i1 %.n7 to i32
  %.a9 = and i32 %i2, %.m8
  %.n10 = xor i1 %i6, true
  %.c11 = and i1 %.n10, %i18
  %.m12 = sext i1 %.c11 to i32
  %.a13 = and i32 %i29, %.m12
  %.o14 = or i32 %.a9, %.a13
  %.m20 = sext i1 %.c11 to i16
  %.a21 = and i16 %i30, %.m20
  %.n15 = xor i1 %i4, true
  %.c35 = and i1 %i6, %.n15
  %.c36 = and i1 %.c35, %i18
  %.m37 = sext i1 %.c36 to i64
  %.a38 = and i64 %i12, %.m37
  %.c41 = and i1 %.n10, %.n15
  %.c42 = and i1 %.c41, %i18
  %.m16 = sext i1 %.n15 to i32
  %.a17 = and i32 %.o14, %.m16
  %i38 = zext i32 %.a17 to i64
  %.sh27 = shl i64 %i38, 29
  %i39 = freeze i64 %.sh27
  %i41 = add i64 %i40, %i39
  %.m18 = sext i1 %.n7 to i16
  %.a19 = and i16 %i17, %.m18
  %.o22 = or i16 %.a19, %.a21
  %.c40 = and i1 %.n15, %.n7
  %.c43 = or i1 %.c40, %.c42
  %.m23 = sext i1 %.n15 to i16
  %.a24 = and i16 %.o22, %.m23
  %i36 = zext i16 %.a24 to i64
  %.sh26 = shl i64 %i36, 52
  %i37 = freeze i64 %.sh26
  %i42 = add i64 %i41, %i37
  %.m44 = sext i1 %.c43 to i64
  %.a45 = and i64 %i42, %.m44
  %.c29 = and i1 %.n10, %i4
  %.c32 = and i1 %i6, %i4
  %.m30 = sext i1 %.c29 to i64
  %.a31 = and i64 %spec.select, %.m30
  %.m33 = sext i1 %.c32 to i64
  %.a34 = and i64 %i13, %.m33
  %.o39 = or i64 %.a34, %.a38
  %.o46 = or i64 %.o39, %.a45
  %.a47 = and i64 9221120237041090560, %.m30
  %.o48 = or i64 %.o46, %.a47
  %i44 = insertvalue [2 x i64] poison, i64 %.a31, 0
  %i45 = insertvalue [2 x i64] %i44, i64 %.o48, 1
  ret [2 x i64] %i45
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
