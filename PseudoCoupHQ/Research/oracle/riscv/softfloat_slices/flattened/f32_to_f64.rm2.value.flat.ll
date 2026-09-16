; ModuleID = '<scratch>/fl/run/f32_to_f64.rm2.value/f32_to_f64.rm2.value.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local i64 @f32_to_f64_rm2_value_flat(i64 %arg) {
  %i = and i64 %arg, 4294967295
  %i1 = trunc i64 %arg to i32
  %i2 = and i32 %i1, 8388607
  %i3 = and i32 %i1, 2139095040
  %i4 = icmp eq i32 %i3, 2139095040
  %.sh1 = lshr i32 %i1, 23
  %i12 = freeze i32 %.sh1
  %i13 = trunc i32 %i12 to i16
  %i14 = and i16 %i13, 255
  %i15 = icmp eq i16 %i14, 0
  %i6 = icmp eq i32 %i2, 0
  %.sh2 = shl i64 %i, 32
  %i8 = freeze i64 %.sh2
  %i9 = and i64 %i8, -9223372036854775808
  %i10 = or i64 %i9, 9218868437227405312
  %i37 = or i64 %i9, 4035225266123964416
  %.k4 = call range(i32 0, 33) i32 @llvm.ctlz.i32(i32 range(i32 1, 8388608) %i2, i1 true)
  %i22 = freeze i32 %.k4
  %i23 = trunc i32 %i22 to i8
  %i24 = add i32 %i22, 248
  %i25 = and i32 %i24, 255
  %.sh5 = shl i32 %i2, %i25
  %i26 = freeze i32 %.sh5
  %narrow = sub i8 8, %i23
  %i27 = sext i8 %narrow to i16
  %.n6 = xor i1 %i15, true
  %.m7 = sext i1 %.n6 to i32
  %.a8 = and i32 %i2, %.m7
  %.n9 = xor i1 %i6, true
  %.c37 = and i1 %i15, %i6
  %.c10 = and i1 %i15, %.n9
  %.m11 = sext i1 %.c10 to i32
  %.a12 = and i32 %i26, %.m11
  %.o13 = or i32 %.a8, %.a12
  %.m19 = sext i1 %.c10 to i16
  %.a20 = and i16 %i27, %.m19
  %.n14 = xor i1 %i4, true
  %.c30 = and i1 %i15, %.n14
  %.c31 = and i1 %.c30, %.n9
  %.c38 = and i1 %.c37, %.n14
  %.m39 = sext i1 %.c38 to i64
  %.a40 = and i64 %i9, %.m39
  %.m15 = sext i1 %.n14 to i32
  %.a16 = and i32 %.o13, %.m15
  %i35 = zext i32 %.a16 to i64
  %.sh26 = shl i64 %i35, 29
  %i36 = freeze i64 %.sh26
  %i38 = add i64 %i37, %i36
  %.m17 = sext i1 %.n6 to i16
  %.a18 = and i16 %i14, %.m17
  %.o21 = or i16 %.a18, %.a20
  %.c32 = and i1 %.n6, %.n14
  %.c33 = or i1 %.c31, %.c32
  %.m22 = sext i1 %.n14 to i16
  %.a23 = and i16 %.o21, %.m22
  %i33 = zext i16 %.a23 to i64
  %.sh25 = shl i64 %i33, 52
  %i34 = freeze i64 %.sh25
  %i39 = add i64 %i38, %i34
  %.m34 = sext i1 %.c33 to i64
  %.a35 = and i64 %i39, %.m34
  %.c27 = and i1 %i6, %i4
  %.m28 = sext i1 %.c27 to i64
  %.a29 = and i64 %i10, %.m28
  %.o36 = or i64 %.a29, %.a35
  %.o41 = or i64 %.o36, %.a40
  %.c43 = and i1 %.n9, %i4
  %.m44 = sext i1 %.c43 to i64
  %.a45 = and i64 9221120237041090560, %.m44
  %.o46 = or i64 %.o41, %.a45
  ret i64 %.o46
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
