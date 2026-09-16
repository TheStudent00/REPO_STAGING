; ModuleID = '<scratch>/fl/run/ui32_to_f16.rm2.flags/ui32_to_f16.rm2.flags.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local i64 @ui32_to_f16_rm2_flags_flat(i32 noundef signext %arg) {
  %i = icmp eq i32 %arg, 0
  %.n14 = xor i1 %i, true
  %.k1 = call range(i32 0, 33) i32 @llvm.ctlz.i32(i32 %arg, i1 true)
  %i2 = freeze i32 %.k1
  %i3 = icmp ult i32 %arg, 2048
  %i13 = add i32 %i2, -17
  %i14 = icmp ugt i32 %arg, 32767
  %i5 = add i32 %i2, 235
  %i6 = and i32 %i5, 255
  %.sh2 = shl i32 %i6, 10
  %.sh3 = shl i32 %arg, %i6
  %i8 = freeze i32 %.sh3
  %i9 = sub i32 %i8, %.sh2
  %i10 = zext i32 %i9 to i64
  %i11 = add i64 %i10, 24576
  %i16 = sub i32 17, %i2
  %.sh4 = lshr i32 %arg, %i16
  %i17 = freeze i32 %.sh4
  %i18 = and i32 %i13, 31
  %.sh5 = shl i32 %arg, %i18
  %i19 = freeze i32 %.sh5
  %i20 = icmp ne i32 %i19, 0
  %i21 = zext i1 %i20 to i32
  %i22 = or i32 %i17, %i21
  %.sh6 = shl i32 %arg, %i13
  %i24 = freeze i32 %.sh6
  %.m7 = sext i1 %i14 to i32
  %.a8 = and i32 %i22, %.m7
  %.n9 = xor i1 %i14, true
  %.m10 = sext i1 %.n9 to i32
  %.a11 = and i32 %i24, %.m10
  %.o12 = or i32 %.a8, %.a11
  %.n13 = xor i1 %i3, true
  %.c47 = and i1 %i3, %.n14
  %.m48 = sext i1 %.c47 to i64
  %.a49 = and i64 %i11, %.m48
  %.m16 = sext i1 %.n13 to i32
  %.a17 = and i32 %.o12, %.m16
  %i27 = sub i32 45, %i2
  %i31 = icmp eq i32 %i2, 16
  %i30 = and i32 %.a17, 32768
  %.not = icmp eq i32 %i30, 0
  %or.cond = and i1 %i31, %.not
  %.a20 = and i32 %i27, %.m10
  %.c21 = and i1 %or.cond, %i14
  %.m22 = sext i1 %.c21 to i32
  %.a23 = and i32 29, %.m22
  %.o24 = or i32 %.a20, %.a23
  %.a25 = and i32 %.o24, %.m16
  %.sh29 = shl i32 %.a25, 10
  %i39 = freeze i32 %.sh29
  %.sh26 = lshr i32 %.a17, 4
  %i34 = freeze i32 %.sh26
  %i35 = and i32 %i34, 4095
  %i36 = and i32 %.a17, 15
  %i37 = icmp eq i32 %i36, 0
  %.m27 = sext i1 %i37 to i64
  %.n28 = xor i64 %.m27, -1
  %spec.select = and i64 1, %.n28
  %i38 = icmp eq i32 %i35, 0
  %.m30 = sext i1 %i38 to i32
  %.n31 = xor i32 %.m30, -1
  %i40 = and i32 %i39, %.n31
  %i41 = add i32 %i35, %i40
  %i42 = zext i32 %i41 to i64
  %.c33 = and i1 %.n13, %or.cond
  %.c34 = and i1 %.c33, %i14
  %.n40 = xor i1 %or.cond, true
  %.c36 = and i1 %.n13, %.n9
  %.c37 = or i1 %.c34, %.c36
  %.c42 = and i1 %.n13, %.n40
  %.c43 = and i1 %.c42, %i14
  %.m38 = sext i1 %.c37 to i64
  %.a39 = and i64 %spec.select, %.m38
  %.a50 = and i64 %i42, %.m38
  %.o51 = or i64 %.a49, %.a50
  %.m44 = sext i1 %.c43 to i64
  %.a45 = and i64 5, %.m44
  %.o46 = or i64 %.a39, %.a45
  %.a52 = and i64 31743, %.m44
  %.o53 = or i64 %.o51, %.a52
  %i44 = shl i64 %.o53, 16
  %i45 = and i64 %i44, 4294901760
  %i46 = or i64 %i45, %.o46
  ret i64 %i46
}

; Function Attrs: nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare i32 @llvm.ctlz.i32(i32, i1 immarg) #0

attributes #0 = { nocallback nofree nosync nounwind speculatable willreturn memory(none) }

!llvm.ident = !{!0, !0, !0, !0, !0, !0, !0, !0}
!llvm.module.flags = !{!1, !2, !3, !5}

!0 = !{!"Ubuntu clang version 21.1.8 (6ubuntu1)"}
!1 = !{i32 1, !"wchar_size", i32 4}
!2 = !{i32 1, !"target-abi", !"lp64"}
!3 = distinct !{i32 6, !"riscv-isa", !4}
!4 = distinct !{!"rv64i2p1_m2p0_zmmul1p0"}
!5 = !{i32 8, !"SmallDataLimit", i32 0}
