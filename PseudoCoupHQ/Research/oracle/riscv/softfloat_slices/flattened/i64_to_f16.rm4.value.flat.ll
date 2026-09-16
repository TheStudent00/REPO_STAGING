; ModuleID = '<scratch>/fl/run/i64_to_f16.rm4.value/i64_to_f16.rm4.value.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local i64 @i64_to_f16_rm4_value_flat(i64 noundef %arg) {
  %i = icmp slt i64 %arg, 0
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
  %.c38 = and i1 %i6, %.n15
  %.m39 = sext i1 %.c38 to i64
  %.a40 = and i64 %i19, %.m39
  %.c16 = and i1 %.n14, %.n15
  %.m17 = sext i1 %.c16 to i64
  %.a18 = and i64 %.o13, %.m17
  %.m31 = sext i1 %.c16 to i32
  %i40 = trunc i64 %.a18 to i32
  %i46 = and i64 %.a18, 65528
  %i47 = icmp ugt i64 %i46, 32759
  %i52 = and i32 %i40, 65528
  %i41 = sext i8 %i21 to i32
  %i42 = sub i32 28, %i41
  %i43 = icmp ugt i8 %i21, 28
  %i45 = icmp ne i8 %i21, -1
  %or.cond = or i1 %i45, %i47
  %.m19 = sext i1 %i to i64
  %.m34 = sext i1 %i to i32
  %i58 = and i32 32768, %.m34
  %.a20 = and i64 64512, %.m19
  %.n21 = xor i64 %.m19, -1
  %.a22 = and i64 31744, %.n21
  %i49 = or i64 %.a20, %.a22
  %.n23 = xor i1 %i43, true
  %.m24 = sext i1 %.n23 to i32
  %.a25 = and i32 %i42, %.m24
  %.c41 = and i1 %.n14, %.n23
  %.c42 = and i1 %.c41, %.n15
  %.n26 = xor i1 %or.cond, true
  %.c50 = and i1 %.n14, %or.cond
  %.c43 = and i1 %.n14, %.n26
  %.m28 = sext i1 %.n26 to i32
  %.a29 = and i32 29, %.m28
  %.o30 = or i32 %.a25, %.a29
  %.a32 = and i32 %.o30, %.m31
  %.sh35 = shl i32 %.a32, 10
  %i59 = freeze i32 %.sh35
  %.c51 = and i1 %.c50, %i43
  %.c45 = and i1 %.c43, %.n15
  %.c46 = or i1 %.c42, %.c45
  %.c52 = and i1 %.c51, %.n15
  %.m47 = sext i1 %.c46 to i64
  %.m53 = sext i1 %.c52 to i64
  %.a54 = and i64 %i49, %.m53
  %i53 = add i32 %i52, 8
  %.sh33 = lshr i32 %i53, 4
  %i54 = freeze i32 %.sh33
  %i61 = or i32 %i54, %i58
  %i57 = icmp eq i32 %i52, 0
  %.m36 = sext i1 %i57 to i32
  %.n37 = xor i32 %.m36, -1
  %i60 = and i32 %i59, %.n37
  %i62 = add i32 %i61, %i60
  %i63 = and i32 %i62, 65535
  %i64 = zext i32 %i63 to i64
  %.a48 = and i64 %i64, %.m47
  %.o49 = or i64 %.a40, %.a48
  %.o55 = or i64 %.o49, %.a54
  %i66 = and i64 %.o55, 65535
  ret i64 %i66
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
