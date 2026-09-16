; ModuleID = '<scratch>/fl/run/i32_to_f16.rm0.flags/i32_to_f16.rm0.flags.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local i64 @i32_to_f16_rm0_flags_flat(i32 noundef signext %arg) {
  %i = icmp slt i32 %arg, 0
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
  %.c53 = and i1 %i5, %.n15
  %.m54 = sext i1 %.c53 to i64
  %.a55 = and i64 %i16, %.m54
  %.c16 = and i1 %.n14, %.n15
  %.m17 = sext i1 %.c16 to i32
  %.a18 = and i32 %.o13, %.m17
  %i32 = sub i32 45, %i4
  %i37 = icmp ne i32 %i4, 16
  %i33 = trunc i32 %.a18 to i8
  %i43 = and i8 %i33, 15
  %i36 = and i32 %.a18, 65528
  %i38 = icmp ugt i32 %i36, 32759
  %or.cond = or i1 %i37, %i38
  %i45 = add i32 %i36, 8
  %.sh32 = lshr i32 %i45, 4
  %i46 = freeze i32 %.sh32
  %.m19 = sext i1 %i to i64
  %.m35 = sext i1 %i to i32
  %i53 = and i32 32768, %.m35
  %.a20 = and i64 64512, %.m19
  %.n21 = xor i64 %.m19, -1
  %.a22 = and i64 31744, %.n21
  %i40 = or i64 %.a20, %.a22
  %.a25 = and i32 %i32, %.m11
  %.c44 = and i1 %.n10, %.n14
  %.c45 = and i1 %.c44, %.n15
  %.n26 = xor i1 %or.cond, true
  %.c39 = and i1 %or.cond, %i19
  %.c41 = and i1 %.c39, %.n15
  %.m42 = sext i1 %.c41 to i64
  %.a56 = and i64 %i40, %.m42
  %.o57 = or i64 %.a55, %.a56
  %.a43 = and i64 5, %.m42
  %.c27 = and i1 %.n26, %i19
  %.c48 = and i1 %.c27, %.n15
  %.c49 = or i1 %.c45, %.c48
  %.m28 = sext i1 %.c27 to i32
  %.a29 = and i32 29, %.m28
  %.o30 = or i32 %.a25, %.a29
  %.a31 = and i32 %.o30, %.m17
  %.sh36 = shl i32 %.a31, 10
  %i54 = freeze i32 %.sh36
  %.m50 = sext i1 %.c49 to i64
  %i47 = icmp eq i8 %i43, 0
  %.m33 = sext i1 %i47 to i64
  %.n34 = xor i64 %.m33, -1
  %spec.select = and i64 1, %.n34
  %i48 = icmp eq i8 %i43, 8
  %i49 = zext i1 %i48 to i32
  %i50 = xor i32 %i49, -1
  %i51 = and i32 %i46, %i50
  %i56 = or i32 %i51, %i53
  %i52 = icmp eq i32 %i51, 0
  %.m37 = sext i1 %i52 to i32
  %.n38 = xor i32 %.m37, -1
  %i55 = and i32 %i54, %.n38
  %i57 = add i32 %i56, %i55
  %i58 = and i32 %i57, 65535
  %i59 = zext i32 %i58 to i64
  %.a51 = and i64 %spec.select, %.m50
  %.o52 = or i64 %.a43, %.a51
  %.a58 = and i64 %i59, %.m50
  %.o59 = or i64 %.o57, %.a58
  %i61 = shl i64 %.o59, 16
  %i62 = and i64 %i61, 4294901760
  %i63 = or i64 %i62, %.o52
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
