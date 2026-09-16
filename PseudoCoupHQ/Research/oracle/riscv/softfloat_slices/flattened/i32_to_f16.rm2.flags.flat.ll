; ModuleID = '<scratch>/fl/run/i32_to_f16.rm2.flags/i32_to_f16.rm2.flags.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local i64 @i32_to_f16_rm2_flags_flat(i32 noundef signext %arg) {
  %i = icmp sgt i32 %arg, -1
  %i1 = call i32 @llvm.abs.i32(i32 %arg, i1 false)
  %i2 = icmp eq i32 %arg, 0
  %.n15 = xor i1 %i2, true
  %.k1 = call range(i32 0, 33) i32 @llvm.ctlz.i32(i32 %i1, i1 true)
  %i4 = freeze i32 %.k1
  %i5 = icmp ult i32 %i1, 2048
  %i18 = add i32 %i4, -17
  %i19 = icmp ugt i32 %i1, 32767
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
  %i16 = zext i32 %i15 to i64
  %i21 = sub i32 17, %i4
  %.sh5 = lshr i32 %i1, %i21
  %i22 = freeze i32 %.sh5
  %i23 = and i32 %i18, 31
  %.sh6 = shl i32 %i1, %i23
  %i24 = freeze i32 %.sh6
  %i25 = icmp ne i32 %i24, 0
  %i26 = zext i1 %i25 to i32
  %i27 = or i32 %i22, %i26
  %.sh7 = shl i32 %i1, %i18
  %i29 = freeze i32 %.sh7
  %.m8 = sext i1 %i19 to i32
  %.a9 = and i32 %i27, %.m8
  %.n10 = xor i1 %i19, true
  %.m11 = sext i1 %.n10 to i32
  %.a12 = and i32 %i29, %.m11
  %.o13 = or i32 %.a9, %.a12
  %.n14 = xor i1 %i5, true
  %.c64 = and i1 %i5, %.n15
  %.m65 = sext i1 %.c64 to i64
  %.a66 = and i64 %i16, %.m65
  %.c16 = and i1 %.n14, %.n15
  %.m17 = sext i1 %.c16 to i32
  %.a18 = and i32 %.o13, %.m17
  %i32 = sub i32 45, %i4
  %i37 = icmp eq i32 %i4, 16
  %.m19 = sext i1 %i to i8
  %.n20 = xor i8 %.m19, -1
  %i33 = and i8 15, %.n20
  %i34 = and i32 %.a18, 65535
  %i39 = zext i8 %i33 to i32
  %i40 = add i32 %i34, %i39
  %i41 = icmp ugt i32 %i40, 32767
  %.m21 = sext i1 %i to i64
  %.m38 = sext i1 %i to i32
  %.n39 = xor i32 %.m38, -1
  %i53 = and i32 32768, %.n39
  %.a22 = and i64 31743, %.m21
  %.n23 = xor i64 %.m21, -1
  %.a24 = and i64 64512, %.n23
  %i43 = or i64 %.a22, %.a24
  %.n25 = xor i1 %i41, true
  %.c26 = and i1 %i19, %i37
  %.c27 = and i1 %.c26, %.n25
  %.m28 = sext i1 %.c27 to i32
  %.a29 = and i32 29, %.m28
  %.a32 = and i32 %i32, %.m11
  %.o33 = or i32 %.a29, %.a32
  %.a34 = and i32 %.o33, %.m17
  %.sh40 = shl i32 %.a34, 10
  %i54 = freeze i32 %.sh40
  %.c54 = and i1 %.n10, %.n14
  %.c55 = and i1 %.c54, %.n15
  %i50 = and i32 %.a18, 15
  %i51 = icmp eq i32 %i50, 0
  %.m36 = sext i1 %i51 to i64
  %.n37 = xor i64 %.m36, -1
  %spec.select = and i64 1, %.n37
  %.sh35 = lshr i32 %i40, 4
  %i49 = freeze i32 %.sh35
  %i56 = or i32 %i49, %i53
  %i52 = icmp ult i32 %i40, 16
  %.m41 = sext i1 %i52 to i32
  %.n42 = xor i32 %.m41, -1
  %i55 = and i32 %i54, %.n42
  %i57 = add i32 %i56, %i55
  %i58 = and i32 %i57, 65535
  %i59 = zext i32 %i58 to i64
  %.n43 = xor i1 %i37, true
  %.c44 = and i1 %i19, %.n43
  %.c46 = and i1 %.c44, %.n15
  %.c49 = and i1 %.c26, %.n15
  %.c50 = and i1 %.c49, %i41
  %.c51 = or i1 %.c46, %.c50
  %.c59 = and i1 %.c49, %.n25
  %.c60 = or i1 %.c55, %.c59
  %.m52 = sext i1 %.c51 to i64
  %.m61 = sext i1 %.c60 to i64
  %.a62 = and i64 %spec.select, %.m61
  %.a69 = and i64 %i59, %.m61
  %.a67 = and i64 %i43, %.m52
  %.o68 = or i64 %.a66, %.a67
  %.o70 = or i64 %.o68, %.a69
  %.a53 = and i64 5, %.m52
  %.o63 = or i64 %.a53, %.a62
  %i61 = shl i64 %.o70, 16
  %i62 = and i64 %i61, 4294901760
  %i63 = or i64 %i62, %.o63
  ret i64 %i63
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
