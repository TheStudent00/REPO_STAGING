; ModuleID = '<scratch>/fl/run/ui64_to_f64.rm1.flags/ui64_to_f64.rm1.flags.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local [2 x i64] @ui64_to_f64_rm1_flags_flat(i64 noundef %arg) {
  %i = icmp eq i64 %arg, 0
  %.n17 = xor i1 %i, true
  %i2 = icmp sgt i64 %arg, -1
  %.k1 = call range(i64 0, 65) i64 @llvm.ctlz.i64(i64 range(i64 1, -9223372036854775808) %arg, i1 true)
  %i10 = freeze i64 %.k1
  %i11 = trunc i64 %i10 to i8
  %i12 = add i8 %i11, -1
  %i19 = add i64 %i10, 4294967285
  %i20 = and i64 %i19, 4294967295
  %.sh5 = shl i64 %arg, %i20
  %i21 = freeze i64 %.sh5
  %i13 = zext i8 %i12 to i16
  %i14 = sub i16 1084, %i13
  %i23 = zext i8 %i12 to i64
  %.sh6 = shl i64 %arg, %i23
  %i24 = freeze i64 %.sh6
  %i15 = icmp ult i64 %arg, 9007199254740992
  %.sh2 = lshr i64 %arg, 1
  %.masked = and i64 %.sh2, 1023
  %i4 = and i64 %arg, 1
  %i6 = or i64 %.masked, %i4
  %i7 = icmp ne i64 %i6, 0
  %.sh3 = lshr i64 %arg, 11
  %i8 = add i64 %.sh3, 4886405595696988160
  %i17 = zext i16 %i14 to i64
  %.sh4 = shl i64 %i17, 52
  %i18 = freeze i64 %.sh4
  %i22 = add i64 %i21, %i18
  %.sh7 = lshr i64 %i24, 10
  %i26 = and i64 %i24, 1023
  %i27 = icmp ne i64 %i26, 0
  %i28 = icmp ult i64 %i24, 1024
  %.m9 = sext i1 %i28 to i64
  %.n10 = xor i64 %.m9, -1
  %i31 = and i64 %i18, %.n10
  %i32 = add i64 %.sh7, %i31
  %.n11 = xor i1 %i15, true
  %.c12 = and i1 %.n11, %i2
  %.a13 = and i1 %i27, %.c12
  %.n14 = xor i1 %i2, true
  %.a15 = and i1 %i7, %.n14
  %.o16 = or i1 %.a13, %.a15
  %.m20 = sext i1 %i15 to i64
  %.a21 = and i64 %i22, %.m20
  %.m22 = sext i1 %.c12 to i64
  %.a23 = and i64 %i32, %.m22
  %.o24 = or i64 %.a21, %.a23
  %.m25 = sext i1 %.n14 to i64
  %.a26 = and i64 %i8, %.m25
  %.o27 = or i64 %.o24, %.a26
  %.m28 = sext i1 %.n17 to i64
  %.a29 = and i64 %.o27, %.m28
  %i34 = zext i1 %.o16 to i64
  %i35 = insertvalue [2 x i64] poison, i64 %i34, 0
  %i36 = insertvalue [2 x i64] %i35, i64 %.a29, 1
  ret [2 x i64] %i36
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
