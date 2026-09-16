; ModuleID = '<scratch>/fl/run/ui64_to_f64.rm4.flags/ui64_to_f64.rm4.flags.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local [2 x i64] @ui64_to_f64_rm4_flags_flat(i64 noundef %arg) {
  %i = icmp eq i64 %arg, 0
  %.n17 = xor i1 %i, true
  %i2 = icmp sgt i64 %arg, -1
  %.k1 = call range(i64 0, 65) i64 @llvm.ctlz.i64(i64 range(i64 1, -9223372036854775808) %arg, i1 true)
  %i11 = freeze i64 %.k1
  %i12 = trunc i64 %i11 to i8
  %i13 = add i8 %i12, -1
  %i20 = add i64 %i11, 4294967285
  %i21 = and i64 %i20, 4294967295
  %.sh5 = shl i64 %arg, %i21
  %i22 = freeze i64 %.sh5
  %i14 = zext i8 %i13 to i16
  %i15 = sub i16 1084, %i14
  %i24 = zext i8 %i13 to i64
  %.sh6 = shl i64 %arg, %i24
  %i25 = freeze i64 %.sh6
  %i16 = icmp ult i64 %arg, 9007199254740992
  %.sh2 = lshr i64 %arg, 1
  %i4 = and i64 %arg, 1
  %i5 = add i64 %.sh2, 512
  %.sh3 = lshr i64 %i5, 10
  %.masked = and i64 %.sh2, 1023
  %i7 = or i64 %.masked, %i4
  %i8 = icmp ne i64 %i7, 0
  %i9 = add i64 %.sh3, 4886405595696988160
  %i18 = zext i16 %i15 to i64
  %.sh4 = shl i64 %i18, 52
  %i19 = freeze i64 %.sh4
  %i23 = add i64 %i22, %i19
  %i26 = add i64 %i25, 512
  %i28 = and i64 %i25, 1023
  %i29 = icmp ne i64 %i28, 0
  %.sh7 = lshr i64 %i26, 10
  %i30 = icmp ult i64 %i26, 1024
  %.m9 = sext i1 %i30 to i64
  %.n10 = xor i64 %.m9, -1
  %i33 = and i64 %i19, %.n10
  %i34 = add i64 %.sh7, %i33
  %.n11 = xor i1 %i16, true
  %.c12 = and i1 %.n11, %i2
  %.a13 = and i1 %i29, %.c12
  %.n14 = xor i1 %i2, true
  %.a15 = and i1 %i8, %.n14
  %.o16 = or i1 %.a13, %.a15
  %.m20 = sext i1 %i16 to i64
  %.a21 = and i64 %i23, %.m20
  %.m22 = sext i1 %.c12 to i64
  %.a23 = and i64 %i34, %.m22
  %.o24 = or i64 %.a21, %.a23
  %.m25 = sext i1 %.n14 to i64
  %.a26 = and i64 %i9, %.m25
  %.o27 = or i64 %.o24, %.a26
  %.m28 = sext i1 %.n17 to i64
  %.a29 = and i64 %.o27, %.m28
  %i36 = zext i1 %.o16 to i64
  %i37 = insertvalue [2 x i64] poison, i64 %i36, 0
  %i38 = insertvalue [2 x i64] %i37, i64 %.a29, 1
  ret [2 x i64] %i38
}

; Function Attrs: nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare i64 @llvm.ctlz.i64(i64, i1 immarg) #0

attributes #0 = { nocallback nofree nosync nounwind speculatable willreturn memory(none) }

!llvm.ident = !{!0, !0, !0, !0, !0, !0, !0, !0, !0}
!llvm.module.flags = !{!1, !2, !3, !5}

!0 = !{!"Ubuntu clang version 21.1.8 (6ubuntu1)"}
!1 = !{i32 1, !"wchar_size", i32 4}
!2 = !{i32 1, !"target-abi", !"lp64"}
!3 = distinct !{i32 6, !"riscv-isa", !4}
!4 = distinct !{!"rv64i2p1_m2p0_zmmul1p0"}
!5 = !{i32 8, !"SmallDataLimit", i32 0}
