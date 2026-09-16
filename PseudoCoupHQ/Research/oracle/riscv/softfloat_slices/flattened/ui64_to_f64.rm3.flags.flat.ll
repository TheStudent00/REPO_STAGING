; ModuleID = '<scratch>/fl/run/ui64_to_f64.rm3.flags/ui64_to_f64.rm3.flags.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local [2 x i64] @ui64_to_f64_rm3_flags_flat(i64 noundef %arg) {
  %i = icmp eq i64 %arg, 0
  %.n17 = xor i1 %i, true
  %i2 = icmp sgt i64 %arg, -1
  %.k1 = call range(i64 0, 65) i64 @llvm.ctlz.i64(i64 range(i64 1, -9223372036854775808) %arg, i1 true)
  %i12 = freeze i64 %.k1
  %i13 = trunc i64 %i12 to i8
  %i14 = add i8 %i13, -1
  %i21 = add i64 %i12, 4294967285
  %i22 = and i64 %i21, 4294967295
  %.sh5 = shl i64 %arg, %i22
  %i23 = freeze i64 %.sh5
  %i15 = zext i8 %i14 to i16
  %i16 = sub i16 1084, %i15
  %i25 = zext i8 %i14 to i64
  %.sh6 = shl i64 %arg, %i25
  %i26 = freeze i64 %.sh6
  %i17 = icmp ult i64 %arg, 9007199254740992
  %.sh2 = lshr i64 %arg, 1
  %i4 = and i64 %arg, 1
  %i5 = or i64 %.sh2, %i4
  %i6 = add i64 %i5, 1023
  %.sh3 = lshr i64 %i6, 10
  %i8 = and i64 %i5, 1023
  %i9 = icmp ne i64 %i8, 0
  %i10 = add i64 %.sh3, 4886405595696988160
  %i19 = zext i16 %i16 to i64
  %.sh4 = shl i64 %i19, 52
  %i20 = freeze i64 %.sh4
  %i24 = add i64 %i23, %i20
  %i27 = add i64 %i26, 1023
  %i29 = and i64 %i26, 1023
  %i30 = icmp ne i64 %i29, 0
  %.sh7 = lshr i64 %i27, 10
  %i31 = icmp ult i64 %i27, 1024
  %.m9 = sext i1 %i31 to i64
  %.n10 = xor i64 %.m9, -1
  %i34 = and i64 %i20, %.n10
  %i35 = add i64 %.sh7, %i34
  %.n11 = xor i1 %i17, true
  %.c12 = and i1 %.n11, %i2
  %.a13 = and i1 %i30, %.c12
  %.n14 = xor i1 %i2, true
  %.a15 = and i1 %i9, %.n14
  %.o16 = or i1 %.a13, %.a15
  %.m20 = sext i1 %i17 to i64
  %.a21 = and i64 %i24, %.m20
  %.m22 = sext i1 %.c12 to i64
  %.a23 = and i64 %i35, %.m22
  %.o24 = or i64 %.a21, %.a23
  %.m25 = sext i1 %.n14 to i64
  %.a26 = and i64 %i10, %.m25
  %.o27 = or i64 %.o24, %.a26
  %.m28 = sext i1 %.n17 to i64
  %.a29 = and i64 %.o27, %.m28
  %i37 = zext i1 %.o16 to i64
  %i38 = insertvalue [2 x i64] poison, i64 %i37, 0
  %i39 = insertvalue [2 x i64] %i38, i64 %.a29, 1
  ret [2 x i64] %i39
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
