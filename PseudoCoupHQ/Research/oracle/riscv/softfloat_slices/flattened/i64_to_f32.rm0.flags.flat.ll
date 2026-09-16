; ModuleID = '<scratch>/fl/run/i64_to_f32.rm0.flags/i64_to_f32.rm0.flags.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local i64 @i64_to_f32_rm0_flags_flat(i64 noundef %arg) {
  %i = icmp slt i64 %arg, 0
  %.m20 = sext i1 %i to i32
  %i48 = and i32 -2147483648, %.m20
  %i1 = call i64 @llvm.abs.i64(i64 %arg, i1 false)
  %i2 = icmp eq i64 %arg, 0
  %.n15 = xor i1 %i2, true
  %.k1 = call range(i64 0, 65) i64 @llvm.ctlz.i64(i64 %i1, i1 true)
  %i4 = freeze i64 %.k1
  %i5 = trunc i64 %i4 to i8
  %i23 = sub i64 33, %i4
  %i24 = and i64 %i23, 255
  %i6 = icmp ult i64 %i1, 16777216
  %i20 = add i8 %i5, -33
  %i8 = add i8 %i5, -40
  %i9 = zext i8 %i8 to i32
  %i21 = icmp ugt i64 %i1, 2147483647
  %.sh2 = lshr i64 %arg, 32
  %i11 = trunc i64 %.sh2 to i32
  %i12 = and i32 %i11, -2147483648
  %i15 = or i32 %i12, 1249902592
  %i13 = trunc i64 %i1 to i32
  %.sh3 = shl i32 %i13, %i9
  %i14 = freeze i32 %.sh3
  %.sh4 = shl i32 %i9, 23
  %i17 = sub i32 %i15, %.sh4
  %i18 = add i32 %i17, %i14
  %.sh5 = lshr i64 %i1, %i24
  %i25 = freeze i64 %.sh5
  %.sh6 = shl i64 -1, %i24
  %i26 = freeze i64 %.sh6
  %i27 = xor i64 %i26, -1
  %i28 = and i64 %i1, %i27
  %i29 = icmp ne i64 %i28, 0
  %i30 = zext i1 %i29 to i64
  %i31 = or i64 %i25, %i30
  %i32 = trunc i64 %i31 to i32
  %i35 = zext i8 %i20 to i32
  %.sh7 = shl i32 %i13, %i35
  %i36 = freeze i32 %.sh7
  %i38 = sext i8 %i20 to i32
  %.sh21 = shl i32 %i38, 23
  %i50 = sub i32 1308622848, %.sh21
  %.m8 = sext i1 %i21 to i32
  %.a9 = and i32 %i32, %.m8
  %.n10 = xor i1 %i21, true
  %.m11 = sext i1 %.n10 to i32
  %.a12 = and i32 %i36, %.m11
  %.o13 = or i32 %.a9, %.a12
  %.n14 = xor i1 %i6, true
  %.m26 = sext i1 %i6 to i32
  %.a27 = and i32 %i18, %.m26
  %.c16 = and i1 %.n14, %.n15
  %.m28 = sext i1 %.n14 to i32
  %.m31 = sext i1 %.n15 to i32
  %.m17 = sext i1 %.c16 to i32
  %.a18 = and i32 %.o13, %.m17
  %.m24 = sext i1 %.c16 to i64
  %i39 = add i32 %.a18, 64
  %.sh19 = lshr i32 %i39, 7
  %i40 = freeze i32 %.sh19
  %i41 = and i32 %.a18, 127
  %i42 = icmp ne i32 %i41, 0
  %i43 = icmp eq i32 %i41, 64
  %i44 = zext i1 %i43 to i32
  %i45 = xor i32 %i44, -1
  %i46 = and i32 %i40, %i45
  %i52 = or i32 %i46, %i48
  %i47 = icmp eq i32 %i46, 0
  %.m22 = sext i1 %i47 to i32
  %.n23 = xor i32 %.m22, -1
  %i51 = and i32 %i50, %.n23
  %i53 = add i32 %i52, %i51
  %.a29 = and i32 %i53, %.m28
  %.o30 = or i32 %.a27, %.a29
  %.a32 = and i32 %.o30, %.m31
  %i54 = zext i1 %i42 to i64
  %.a25 = and i64 %i54, %.m24
  %i56 = zext i32 %.a32 to i64
  %i57 = shl i64 %i56, 32
  %i58 = or i64 %i57, %.a25
  ret i64 %i58
}

; Function Attrs: nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare i64 @llvm.abs.i64(i64, i1 immarg) #0

; Function Attrs: nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare i64 @llvm.ctlz.i64(i64, i1 immarg) #0

attributes #0 = { nocallback nofree nosync nounwind speculatable willreturn memory(none) }

!llvm.ident = !{!0, !0, !0, !0, !0, !0, !0, !0}
!llvm.module.flags = !{!1, !2, !3, !5}

!0 = !{!"Ubuntu clang version 21.1.8 (6ubuntu1)"}
!1 = !{i32 1, !"wchar_size", i32 4}
!2 = !{i32 1, !"target-abi", !"lp64"}
!3 = distinct !{i32 6, !"riscv-isa", !4}
!4 = distinct !{!"rv64i2p1_m2p0_zmmul1p0"}
!5 = !{i32 8, !"SmallDataLimit", i32 0}
