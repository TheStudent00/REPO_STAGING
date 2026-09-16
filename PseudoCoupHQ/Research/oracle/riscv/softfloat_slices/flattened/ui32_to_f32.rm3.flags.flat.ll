; ModuleID = '<scratch>/fl/run/ui32_to_f32.rm3.flags/ui32_to_f32.rm3.flags.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local i64 @ui32_to_f32_rm3_flags_flat(i32 noundef signext %arg) {
  %i = icmp eq i32 %arg, 0
  %.n17 = xor i1 %i, true
  %i2 = icmp sgt i32 %arg, -1
  %.k1 = call range(i32 0, 33) i32 @llvm.ctlz.i32(i32 range(i32 1, -2147483648) %arg, i1 true)
  %i12 = freeze i32 %.k1
  %i13 = trunc i32 %i12 to i8
  %i14 = add i8 %i13, -1
  %i15 = zext i8 %i14 to i32
  %i16 = zext i8 %i14 to i16
  %i17 = sub i16 156, %i16
  %i18 = icmp ult i32 %arg, 16777216
  %.sh2 = lshr i32 %arg, 1
  %i4 = and i32 %arg, 1
  %i5 = or i32 %.sh2, %i4
  %i6 = add i32 %i5, 127
  %.sh3 = lshr i32 %i6, 7
  %i8 = and i32 %i5, 127
  %i9 = icmp ne i32 %i8, 0
  %i10 = add i32 %.sh3, 1317011456
  %i20 = zext i16 %i17 to i32
  %.sh4 = shl i32 %i20, 23
  %i21 = freeze i32 %.sh4
  %i22 = add i32 %i15, -7
  %.sh5 = shl i32 %arg, %i22
  %i23 = freeze i32 %.sh5
  %i24 = add i32 %i23, %i21
  %.sh6 = shl i32 %arg, %i15
  %i25 = freeze i32 %.sh6
  %i26 = add i32 %i25, 127
  %i28 = and i32 %i25, 127
  %i29 = icmp ne i32 %i28, 0
  %.sh7 = lshr i32 %i26, 7
  %i30 = icmp ult i32 %i26, 128
  %.m9 = sext i1 %i30 to i32
  %.n10 = xor i32 %.m9, -1
  %i33 = and i32 %i21, %.n10
  %i34 = add i32 %.sh7, %i33
  %.n11 = xor i1 %i18, true
  %.c12 = and i1 %.n11, %i2
  %.a13 = and i1 %i29, %.c12
  %.n14 = xor i1 %i2, true
  %.a15 = and i1 %i9, %.n14
  %.o16 = or i1 %.a13, %.a15
  %.m20 = sext i1 %i18 to i32
  %.a21 = and i32 %i24, %.m20
  %.m22 = sext i1 %.c12 to i32
  %.a23 = and i32 %i34, %.m22
  %.o24 = or i32 %.a21, %.a23
  %.m25 = sext i1 %.n14 to i32
  %.a26 = and i32 %i10, %.m25
  %.o27 = or i32 %.o24, %.a26
  %.m28 = sext i1 %.n17 to i32
  %.a29 = and i32 %.o27, %.m28
  %i35 = zext i32 %.a29 to i64
  %i36 = shl i64 %i35, 32
  %i37 = zext i1 %.o16 to i64
  %i38 = or i64 %i36, %i37
  ret i64 %i38
}

; Function Attrs: nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare i32 @llvm.ctlz.i32(i32, i1 immarg) #0

attributes #0 = { nocallback nofree nosync nounwind speculatable willreturn memory(none) }

!llvm.ident = !{!0, !0, !0, !0, !0, !0, !0, !0, !0}
!llvm.module.flags = !{!1, !2, !3, !5}

!0 = !{!"Ubuntu clang version 21.1.8 (6ubuntu1)"}
!1 = !{i32 1, !"wchar_size", i32 4}
!2 = !{i32 1, !"target-abi", !"lp64"}
!3 = distinct !{i32 6, !"riscv-isa", !4}
!4 = distinct !{!"rv64i2p1_m2p0_zmmul1p0"}
!5 = !{i32 8, !"SmallDataLimit", i32 0}
