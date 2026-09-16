; ModuleID = '<scratch>/fl/run/ui64_to_f64.rm0.flags/ui64_to_f64.rm0.flags.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local [2 x i64] @ui64_to_f64_rm0_flags_flat(i64 noundef %arg) {
  %i = icmp eq i64 %arg, 0
  %.n19 = xor i1 %i, true
  %i2 = icmp sgt i64 %arg, -1
  %.k1 = call range(i64 0, 65) i64 @llvm.ctlz.i64(i64 range(i64 1, -9223372036854775808) %arg, i1 true)
  %i19 = freeze i64 %.k1
  %i20 = trunc i64 %i19 to i8
  %i21 = add i8 %i20, -1
  %i28 = add i64 %i19, 4294967285
  %i29 = and i64 %i28, 4294967295
  %.sh7 = shl i64 %arg, %i29
  %i30 = freeze i64 %.sh7
  %i22 = zext i8 %i21 to i16
  %i23 = sub i16 1084, %i22
  %i32 = zext i8 %i21 to i64
  %.sh8 = shl i64 %arg, %i32
  %i33 = freeze i64 %.sh8
  %i24 = icmp ult i64 %arg, 9007199254740992
  %.sh2 = lshr i64 %arg, 1
  %i4 = and i64 %arg, 1
  %i5 = or i64 %.sh2, %i4
  %i6 = trunc i64 %i5 to i16
  %i7 = and i16 %i6, 1023
  %i8 = add i64 %.sh2, 512
  %.sh3 = lshr i64 %i8, 10
  %i10 = icmp ne i16 %i7, 0
  %i11 = icmp eq i16 %i7, 512
  %i12 = zext i1 %i11 to i64
  %i13 = xor i64 %i12, -1
  %i14 = and i64 %.sh3, %i13
  %i15 = icmp eq i64 %i14, 0
  %.m4 = sext i1 %i15 to i64
  %.n5 = xor i64 %.m4, -1
  %i16 = and i64 4886405595696988160, %.n5
  %i17 = add i64 %i14, %i16
  %i26 = zext i16 %i23 to i64
  %.sh6 = shl i64 %i26, 52
  %i27 = freeze i64 %.sh6
  %i31 = add i64 %i30, %i27
  %i34 = trunc i64 %i33 to i16
  %i35 = and i16 %i34, 1023
  %i36 = add i64 %i33, 512
  %.sh9 = lshr i64 %i36, 10
  %i38 = icmp ne i16 %i35, 0
  %i39 = icmp eq i16 %i35, 512
  %i40 = zext i1 %i39 to i64
  %i41 = xor i64 %i40, -1
  %i42 = and i64 %.sh9, %i41
  %i43 = icmp eq i64 %i42, 0
  %.m11 = sext i1 %i43 to i64
  %.n12 = xor i64 %.m11, -1
  %i46 = and i64 %i27, %.n12
  %i47 = add i64 %i42, %i46
  %.n13 = xor i1 %i24, true
  %.c14 = and i1 %.n13, %i2
  %.a15 = and i1 %i38, %.c14
  %.n16 = xor i1 %i2, true
  %.a17 = and i1 %i10, %.n16
  %.o18 = or i1 %.a15, %.a17
  %.m22 = sext i1 %i24 to i64
  %.a23 = and i64 %i31, %.m22
  %.m24 = sext i1 %.c14 to i64
  %.a25 = and i64 %i47, %.m24
  %.o26 = or i64 %.a23, %.a25
  %.m27 = sext i1 %.n16 to i64
  %.a28 = and i64 %i17, %.m27
  %.o29 = or i64 %.o26, %.a28
  %.m30 = sext i1 %.n19 to i64
  %.a31 = and i64 %.o29, %.m30
  %i49 = zext i1 %.o18 to i64
  %i50 = insertvalue [2 x i64] poison, i64 %i49, 0
  %i51 = insertvalue [2 x i64] %i50, i64 %.a31, 1
  ret [2 x i64] %i51
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
