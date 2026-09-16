; ModuleID = '<scratch>/fl/run/ui32_to_f32.rm0.flags/ui32_to_f32.rm0.flags.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local i64 @ui32_to_f32_rm0_flags_flat(i32 noundef signext %arg) {
  %i = icmp eq i32 %arg, 0
  %.n19 = xor i1 %i, true
  %i2 = icmp sgt i32 %arg, -1
  %.k1 = call range(i32 0, 33) i32 @llvm.ctlz.i32(i32 range(i32 1, -2147483648) %arg, i1 true)
  %i17 = freeze i32 %.k1
  %i18 = trunc i32 %i17 to i8
  %i19 = add i8 %i18, -1
  %i20 = zext i8 %i19 to i32
  %i21 = zext i8 %i19 to i16
  %i22 = sub i16 156, %i21
  %i23 = icmp ult i32 %arg, 16777216
  %.sh2 = lshr i32 %arg, 1
  %i4 = and i32 %arg, 1
  %i5 = add i32 %.sh2, 64
  %.sh3 = lshr i32 %i5, 7
  %.masked = and i32 %.sh2, 127
  %i7 = or i32 %.masked, %i4
  %i8 = icmp ne i32 %i7, 0
  %i9 = icmp eq i32 %i7, 64
  %i10 = zext i1 %i9 to i32
  %i11 = xor i32 %i10, -1
  %i12 = and i32 %.sh3, %i11
  %i13 = icmp eq i32 %i12, 0
  %.m4 = sext i1 %i13 to i32
  %.n5 = xor i32 %.m4, -1
  %i14 = and i32 1317011456, %.n5
  %i15 = add i32 %i12, %i14
  %i25 = zext i16 %i22 to i32
  %.sh6 = shl i32 %i25, 23
  %i26 = freeze i32 %.sh6
  %i27 = add i32 %i20, -7
  %.sh7 = shl i32 %arg, %i27
  %i28 = freeze i32 %.sh7
  %i29 = add i32 %i28, %i26
  %.sh8 = shl i32 %arg, %i20
  %i30 = freeze i32 %.sh8
  %i31 = add i32 %i30, 64
  %.sh9 = lshr i32 %i31, 7
  %i33 = and i32 %i30, 127
  %i34 = icmp ne i32 %i33, 0
  %i35 = icmp eq i32 %i33, 64
  %i36 = zext i1 %i35 to i32
  %i37 = xor i32 %i36, -1
  %i38 = and i32 %.sh9, %i37
  %i39 = icmp eq i32 %i38, 0
  %.m11 = sext i1 %i39 to i32
  %.n12 = xor i32 %.m11, -1
  %i42 = and i32 %i26, %.n12
  %i43 = add i32 %i38, %i42
  %.n13 = xor i1 %i23, true
  %.c14 = and i1 %i2, %.n13
  %.a15 = and i1 %i34, %.c14
  %.n16 = xor i1 %i2, true
  %.a17 = and i1 %i8, %.n16
  %.o18 = or i1 %.a15, %.a17
  %.m22 = sext i1 %i23 to i32
  %.a23 = and i32 %i29, %.m22
  %.m24 = sext i1 %.c14 to i32
  %.a25 = and i32 %i43, %.m24
  %.o26 = or i32 %.a23, %.a25
  %.m27 = sext i1 %.n16 to i32
  %.a28 = and i32 %i15, %.m27
  %.o29 = or i32 %.o26, %.a28
  %.m30 = sext i1 %.n19 to i32
  %.a31 = and i32 %.o29, %.m30
  %i44 = zext i32 %.a31 to i64
  %i45 = shl i64 %i44, 32
  %i46 = zext i1 %.o18 to i64
  %i47 = or i64 %i45, %i46
  ret i64 %i47
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
