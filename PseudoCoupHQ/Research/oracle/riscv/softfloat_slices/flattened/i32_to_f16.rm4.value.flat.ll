; ModuleID = '<scratch>/fl/run/i32_to_f16.rm4.value/i32_to_f16.rm4.value.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local i64 @i32_to_f16_rm4_value_flat(i32 noundef signext %arg) {
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
  %.c37 = and i1 %i5, %.n15
  %.m38 = sext i1 %.c37 to i64
  %.a39 = and i64 %i16, %.m38
  %.c16 = and i1 %.n14, %.n15
  %.m17 = sext i1 %.c16 to i32
  %.a18 = and i32 %.o13, %.m17
  %i32 = sub i32 45, %i4
  %i36 = icmp ne i32 %i4, 16
  %i35 = and i32 %.a18, 65528
  %i37 = icmp ugt i32 %i35, 32759
  %or.cond = or i1 %i36, %i37
  %.m19 = sext i1 %i to i64
  %.m33 = sext i1 %i to i32
  %i48 = and i32 32768, %.m33
  %.a20 = and i64 64512, %.m19
  %.n21 = xor i64 %.m19, -1
  %.a22 = and i64 31744, %.n21
  %i39 = or i64 %.a20, %.a22
  %.a25 = and i32 %i32, %.m11
  %.c40 = and i1 %.n10, %.n14
  %.c41 = and i1 %.c40, %.n15
  %.n26 = xor i1 %or.cond, true
  %.c49 = and i1 %i19, %or.cond
  %.c51 = and i1 %.c49, %.n15
  %.m52 = sext i1 %.c51 to i64
  %.a53 = and i64 %i39, %.m52
  %.c27 = and i1 %i19, %.n26
  %.c44 = and i1 %.c27, %.n15
  %.c45 = or i1 %.c41, %.c44
  %.m28 = sext i1 %.c27 to i32
  %.a29 = and i32 29, %.m28
  %.o30 = or i32 %.a25, %.a29
  %.a31 = and i32 %.o30, %.m17
  %.sh34 = shl i32 %.a31, 10
  %i49 = freeze i32 %.sh34
  %.m46 = sext i1 %.c45 to i64
  %i43 = add i32 %i35, 8
  %.sh32 = lshr i32 %i43, 4
  %i44 = freeze i32 %.sh32
  %i51 = or i32 %i44, %i48
  %i47 = icmp eq i32 %i35, 0
  %.m35 = sext i1 %i47 to i32
  %.n36 = xor i32 %.m35, -1
  %i50 = and i32 %i49, %.n36
  %i52 = add i32 %i51, %i50
  %i53 = and i32 %i52, 65535
  %i54 = zext i32 %i53 to i64
  %.a47 = and i64 %i54, %.m46
  %.o48 = or i64 %.a39, %.a47
  %.o54 = or i64 %.o48, %.a53
  %i56 = and i64 %.o54, 65535
  ret i64 %i56
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
