; ModuleID = '<scratch>/fl/run/i64_to_f32.rm3.value/i64_to_f32.rm3.value.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local i64 @i64_to_f32_rm3_value_flat(i64 noundef %arg) {
  %i = icmp sgt i64 %arg, -1
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
  %.sh23 = shl i32 %i38, 23
  %i47 = sub i32 1308622848, %.sh23
  %.m8 = sext i1 %i21 to i32
  %.a9 = and i32 %i32, %.m8
  %.n10 = xor i1 %i21, true
  %.m11 = sext i1 %.n10 to i32
  %.a12 = and i32 %i36, %.m11
  %.o13 = or i32 %.a9, %.a12
  %.n14 = xor i1 %i6, true
  %.m28 = sext i1 %i6 to i32
  %.a29 = and i32 %i18, %.m28
  %.c16 = and i1 %.n14, %.n15
  %.m17 = sext i1 %.c16 to i32
  %.a18 = and i32 %.o13, %.m17
  %.m26 = sext i1 %.n14 to i32
  %.m31 = sext i1 %.n15 to i32
  %.m19 = sext i1 %i to i32
  %i39 = and i32 127, %.m19
  %i40 = add i32 %.a18, %i39
  %.n22 = xor i32 %.m19, -1
  %i45 = and i32 -2147483648, %.n22
  %.sh20 = lshr i32 %i40, 7
  %i41 = freeze i32 %.sh20
  %i49 = or i32 %i41, %i45
  %i44 = icmp ult i32 %i40, 128
  %.m24 = sext i1 %i44 to i32
  %.n25 = xor i32 %.m24, -1
  %i48 = and i32 %i47, %.n25
  %i50 = add i32 %i49, %i48
  %.a27 = and i32 %i50, %.m26
  %.o30 = or i32 %.a27, %.a29
  %.a32 = and i32 %.o30, %.m31
  %i52 = zext i32 %.a32 to i64
  ret i64 %i52
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
