; ModuleID = '<scratch>/fl/run/i32_to_f16.rm3.value/i32_to_f16.rm3.value.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local i64 @i32_to_f16_rm3_value_flat(i32 noundef signext %arg) {
  %i = icmp slt i32 %arg, 0
  %i1 = call i32 @llvm.abs.i32(i32 %arg, i1 false)
  %i2 = icmp eq i32 %arg, 0
  %.n15 = xor i1 %i2, true
  %.k1 = call range(i32 0, 33) i32 @llvm.ctlz.i32(i32 %i1, i1 true)
  %i4 = freeze i32 %.k1
  %i5 = icmp ult i32 %i1, 2048
  %i19 = add i32 %i4, -17
  %i20 = icmp ugt i32 %i1, 32767
  %i7 = add i32 %i4, 235
  %i10 = and i32 %i7, 255
  %.sh2 = lshr i32 %arg, 16
  %i9 = and i32 %.sh2, 32768
  %i12 = or i32 %i9, 24576
  %.sh3 = shl i32 %i1, %i10
  %i11 = freeze i32 %.sh3
  %.sh4 = shl i32 %i10, 10
  %i14 = sub i32 %i12, %.sh4
  %i15 = add i32 %i14, %i11
  %i16 = and i32 %i15, 65535
  %i17 = zext i32 %i16 to i64
  %i22 = sub i32 17, %i4
  %.sh5 = lshr i32 %i1, %i22
  %i23 = freeze i32 %.sh5
  %i24 = and i32 %i19, 31
  %.sh6 = shl i32 %i1, %i24
  %i25 = freeze i32 %.sh6
  %i26 = icmp ne i32 %i25, 0
  %i27 = zext i1 %i26 to i32
  %i28 = or i32 %i23, %i27
  %.sh7 = shl i32 %i1, %i19
  %i30 = freeze i32 %.sh7
  %.m8 = sext i1 %i20 to i32
  %.a9 = and i32 %i28, %.m8
  %.n10 = xor i1 %i20, true
  %.m11 = sext i1 %.n10 to i32
  %.a12 = and i32 %i30, %.m11
  %.o13 = or i32 %.a9, %.a12
  %.n14 = xor i1 %i5, true
  %.m64 = sext i1 %i5 to i64
  %.a65 = and i64 %i17, %.m64
  %.c16 = and i1 %.n14, %.n15
  %.m17 = sext i1 %.c16 to i32
  %.a18 = and i32 %.o13, %.m17
  %i33 = sub i32 45, %i4
  %i38 = icmp eq i32 %i4, 16
  %.m19 = sext i1 %i to i8
  %.n20 = xor i8 %.m19, -1
  %i34 = and i8 15, %.n20
  %i35 = and i32 %.a18, 65535
  %i40 = zext i8 %i34 to i32
  %i41 = add i32 %i35, %i40
  %i42 = icmp ugt i32 %i41, 32767
  %.m21 = sext i1 %i to i64
  %.m37 = sext i1 %i to i32
  %i56 = and i32 32768, %.m37
  %.a22 = and i64 64512, %.m21
  %.n23 = xor i64 %.m21, -1
  %.a24 = and i64 31744, %.n23
  %i44 = or i64 %.a22, %.a24
  %.sh25 = ashr i32 %arg, 31
  %i45 = sext i32 %.sh25 to i64
  %i46 = add i64 %i44, %i45
  %.n26 = xor i1 %i42, true
  %.c54 = and i1 %i42, %i20
  %.c55 = and i1 %.c54, %i38
  %.c57 = and i1 %.c55, %.n15
  %.c27 = and i1 %.n26, %i20
  %.c28 = and i1 %.c27, %i38
  %.m29 = sext i1 %.c28 to i32
  %.a30 = and i32 29, %.m29
  %.c46 = and i1 %.c28, %.n15
  %.n50 = xor i1 %i38, true
  %.c51 = and i1 %i20, %.n50
  %.c53 = and i1 %.c51, %.n15
  %.c58 = or i1 %.c53, %.c57
  %.m59 = sext i1 %.c58 to i64
  %.a60 = and i64 %i46, %.m59
  %.a33 = and i32 %i33, %.m11
  %.o34 = or i32 %.a30, %.a33
  %.a35 = and i32 %.o34, %.m17
  %.sh38 = shl i32 %.a35, 10
  %i57 = freeze i32 %.sh38
  %.c41 = and i1 %.n10, %.n14
  %.c42 = and i1 %.c41, %.n15
  %.c47 = or i1 %.c42, %.c46
  %.m48 = sext i1 %.c47 to i64
  %.m62 = sext i1 %.n14 to i64
  %.m67 = sext i1 %.n15 to i64
  %.sh36 = lshr i32 %i41, 4
  %i52 = freeze i32 %.sh36
  %i59 = or i32 %i52, %i56
  %i55 = icmp ult i32 %i41, 16
  %.m39 = sext i1 %i55 to i32
  %.n40 = xor i32 %.m39, -1
  %i58 = and i32 %i57, %.n40
  %i60 = add i32 %i59, %i58
  %i61 = zext i32 %i60 to i64
  %.a49 = and i64 %i61, %.m48
  %.o61 = or i64 %.a49, %.a60
  %i63 = and i64 %.o61, 65535
  %.a63 = and i64 %i63, %.m62
  %.o66 = or i64 %.a63, %.a65
  %.a68 = and i64 %.o66, %.m67
  ret i64 %.a68
}

; Function Attrs: nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare i32 @llvm.abs.i32(i32, i1 immarg) #0

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
