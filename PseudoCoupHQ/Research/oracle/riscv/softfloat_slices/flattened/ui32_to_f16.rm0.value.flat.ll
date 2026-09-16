; ModuleID = '<scratch>/fl/run/ui32_to_f16.rm0.value/ui32_to_f16.rm0.value.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local i64 @ui32_to_f16_rm0_value_flat(i32 noundef signext %arg) {
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
  %.c31 = and i1 %i3, %.n14
  %.m32 = sext i1 %.c31 to i64
  %.a33 = and i64 %i11, %.m32
  %.m16 = sext i1 %.n13 to i32
  %.a17 = and i32 %.o12, %.m16
  %i27 = sub i32 45, %i2
  %i32 = icmp ne i32 %i2, 16
  %i28 = trunc i32 %.a17 to i8
  %i36 = and i8 %i28, 15
  %i41 = icmp eq i8 %i36, 8
  %i42 = zext i1 %i41 to i32
  %i43 = xor i32 %i42, -1
  %i31 = and i32 %.a17, 65528
  %i33 = icmp ugt i32 %i31, 32759
  %or.cond = or i1 %i32, %i33
  %i38 = add i32 %i31, 8
  %.sh27 = lshr i32 %i38, 4
  %i39 = freeze i32 %.sh27
  %i44 = and i32 %i39, %i43
  %.a20 = and i32 %i27, %.m10
  %.c34 = and i1 %.n13, %.n9
  %.n21 = xor i1 %or.cond, true
  %.c22 = and i1 %i14, %.n21
  %.m23 = sext i1 %.c22 to i32
  %.a24 = and i32 29, %.m23
  %.o25 = or i32 %.a20, %.a24
  %.a26 = and i32 %.o25, %.m16
  %.sh28 = shl i32 %.a26, 10
  %i46 = freeze i32 %.sh28
  %i45 = icmp eq i32 %i44, 0
  %.m29 = sext i1 %i45 to i32
  %.n30 = xor i32 %.m29, -1
  %i47 = and i32 %i46, %.n30
  %i48 = add i32 %i44, %i47
  %i49 = zext i32 %i48 to i64
  %.c39 = or i1 %.c34, %.c22
  %.c45 = and i1 %i14, %or.cond
  %.m40 = sext i1 %.c39 to i64
  %.a41 = and i64 %i49, %.m40
  %.o42 = or i64 %.a33, %.a41
  %.m46 = sext i1 %.c45 to i64
  %.a47 = and i64 31744, %.m46
  %.o48 = or i64 %.o42, %.a47
  %i51 = and i64 %.o48, 65535
  ret i64 %i51
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
