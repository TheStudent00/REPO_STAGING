; ModuleID = '<scratch>/fl/run/i64_to_f16.rm2.value/i64_to_f16.rm2.value.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local i64 @i64_to_f16_rm2_value_flat(i64 noundef %arg) {
  %i = icmp sgt i64 %arg, -1
  %i1 = call i64 @llvm.abs.i64(i64 %arg, i1 false)
  %i2 = icmp eq i64 %arg, 0
  %.n15 = xor i1 %i2, true
  %.k1 = call range(i64 0, 65) i64 @llvm.ctlz.i64(i64 %i1, i1 true)
  %i4 = freeze i64 %.k1
  %i5 = trunc i64 %i4 to i8
  %i24 = sub i64 49, %i4
  %i25 = and i64 %i24, 255
  %i6 = icmp ult i64 %i1, 2048
  %i21 = add i8 %i5, -49
  %i8 = add i8 %i5, -53
  %i12 = zext i8 %i8 to i32
  %i22 = icmp ugt i64 %i1, 32767
  %.sh2 = lshr i64 %arg, 48
  %i10 = trunc i64 %.sh2 to i32
  %i11 = and i32 %i10, 32768
  %i15 = or i32 %i11, 24576
  %i13 = trunc i64 %i1 to i32
  %.sh3 = shl i32 %i13, %i12
  %i14 = freeze i32 %.sh3
  %.sh4 = shl i32 %i12, 10
  %i17 = sub i32 %i15, %.sh4
  %i18 = add i32 %i17, %i14
  %i19 = zext i32 %i18 to i64
  %.sh5 = lshr i64 %i1, %i25
  %i26 = freeze i64 %.sh5
  %.sh6 = shl i64 -1, %i25
  %i27 = freeze i64 %.sh6
  %i28 = xor i64 %i27, -1
  %i29 = and i64 %i1, %i28
  %i30 = icmp ne i64 %i29, 0
  %i31 = zext i1 %i30 to i64
  %i32 = or i64 %i26, %i31
  %i35 = zext i8 %i21 to i32
  %.sh7 = shl i32 %i13, %i35
  %i36 = freeze i32 %.sh7
  %i37 = zext i32 %i36 to i64
  %.m8 = sext i1 %i22 to i64
  %.a9 = and i64 %i32, %.m8
  %.n10 = xor i1 %i22, true
  %.m11 = sext i1 %.n10 to i64
  %.a12 = and i64 %i37, %.m11
  %.o13 = or i64 %.a9, %.a12
  %.n14 = xor i1 %i6, true
  %.c42 = and i1 %i6, %.n15
  %.m43 = sext i1 %.c42 to i64
  %.a44 = and i64 %i19, %.m43
  %.c16 = and i1 %.n14, %.n15
  %.m17 = sext i1 %.c16 to i64
  %.a18 = and i64 %.o13, %.m17
  %.m34 = sext i1 %.c16 to i32
  %i40 = trunc i64 %.a18 to i32
  %i45 = and i32 %i40, 65535
  %i41 = sext i8 %i21 to i32
  %i42 = sub i32 28, %i41
  %.m19 = sext i1 %i to i8
  %.n20 = xor i8 %.m19, -1
  %i43 = and i8 15, %.n20
  %i46 = icmp ugt i8 %i21, 28
  %i48 = icmp eq i8 %i21, -1
  %i50 = zext i8 %i43 to i32
  %i51 = add i32 %i45, %i50
  %i52 = icmp ugt i32 %i51, 32767
  %.m21 = sext i1 %i to i64
  %.m37 = sext i1 %i to i32
  %.n38 = xor i32 %.m37, -1
  %i64 = and i32 32768, %.n38
  %.a22 = and i64 31743, %.m21
  %.n23 = xor i64 %.m21, -1
  %.a24 = and i64 64512, %.n23
  %i54 = or i64 %.a22, %.a24
  %.n25 = xor i1 %i52, true
  %.c26 = and i1 %i48, %.n25
  %.m28 = sext i1 %.c26 to i32
  %.a29 = and i32 29, %.m28
  %.n30 = xor i1 %i46, true
  %.m31 = sext i1 %.n30 to i32
  %.a32 = and i32 %i42, %.m31
  %.o33 = or i32 %.a29, %.a32
  %.a35 = and i32 %.o33, %.m34
  %.sh39 = shl i32 %.a35, 10
  %i65 = freeze i32 %.sh39
  %.sh36 = lshr i32 %i51, 4
  %i60 = freeze i32 %.sh36
  %i67 = or i32 %i60, %i64
  %i63 = icmp ult i32 %i51, 16
  %.m40 = sext i1 %i63 to i32
  %.n41 = xor i32 %.m40, -1
  %i66 = and i32 %i65, %.n41
  %i68 = add i32 %i67, %i66
  %i69 = and i32 %i68, 65535
  %i70 = zext i32 %i69 to i64
  %.c46 = and i1 %.c16, %.n30
  %.c47 = and i1 %.n14, %i48
  %.c48 = and i1 %.c47, %.n25
  %.c49 = and i1 %.c48, %.n15
  %.c51 = or i1 %.c46, %.c49
  %.m52 = sext i1 %.c51 to i64
  %.a53 = and i64 %i70, %.m52
  %.o54 = or i64 %.a44, %.a53
  %.n55 = xor i1 %i48, true
  %.c56 = and i1 %.n14, %.n55
  %.c60 = and i1 %.c47, %i52
  %.c57 = and i1 %.c56, %.n15
  %.c61 = and i1 %.c60, %.n15
  %.c58 = and i1 %.c57, %i46
  %.c63 = or i1 %.c58, %.c61
  %.m64 = sext i1 %.c63 to i64
  %.a65 = and i64 %i54, %.m64
  %.o66 = or i64 %.o54, %.a65
  %i72 = and i64 %.o66, 65535
  ret i64 %i72
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
