; ModuleID = '<scratch>/fl/run/i32_to_f32.rm3.value/i32_to_f32.rm3.value.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local i64 @i32_to_f32_rm3_value_flat(i32 noundef signext %arg) {
  %i = icmp sgt i32 %arg, -1
  %i1 = and i32 %arg, 2147483647
  %i2 = icmp eq i32 %i1, 0
  %.m1 = sext i1 %i to i64
  %.n2 = xor i64 %.m1, -1
  %i4 = and i64 3472883712, %.n2
  %.m19 = sext i1 %i to i32
  %i28 = and i32 127, %.m19
  %.k3 = call i32 @llvm.abs.i32(i32 %arg, i1 false)
  %i7 = icmp eq i32 %arg, 0
  %.k4 = call range(i32 0, 33) i32 @llvm.ctlz.i32(i32 range(i32 0, -2147483647) %.k3, i1 true)
  %i9 = freeze i32 %.k4
  %i10 = trunc i32 %i9 to i8
  %i11 = add i8 %i10, -1
  %.n5 = xor i1 %i7, true
  %.m6 = sext i1 %.n5 to i8
  %.a7 = and i8 %i11, %.m6
  %.m8 = sext i1 %i7 to i8
  %.a9 = and i8 31, %.m8
  %.o10 = or i8 %.a7, %.a9
  %.m15 = sext i1 %i7 to i32
  %.n16 = xor i32 %.m15, -1
  %.n11 = xor i1 %i2, true
  %.m34 = sext i1 %i2 to i64
  %.a35 = and i64 %i4, %.m34
  %.m12 = sext i1 %.n11 to i8
  %.a13 = and i8 %.o10, %.m12
  %i14 = sext i8 %.a13 to i32
  %i15 = sext i8 %.a13 to i16
  %i16 = sub i16 156, %i15
  %i17 = icmp sgt i8 %.a13, 6
  %i19 = zext i16 %i16 to i32
  %.sh14 = shl i32 %i19, 23
  %i21 = freeze i32 %.sh14
  %i22 = and i32 %i21, %.n16
  %i20 = and i32 %arg, -2147483648
  %i23 = add i32 %i14, -7
  %.sh17 = shl i32 %.k3, %i23
  %.sh18 = shl i32 %.k3, %i14
  %i24 = freeze i32 %.sh17
  %i25 = add i32 %i24, %i20
  %i26 = add i32 %i25, %i22
  %i27 = freeze i32 %.sh18
  %i29 = add i32 %i27, %i28
  %.sh20 = lshr i32 %i29, 7
  %i33 = icmp ult i32 %i29, 128
  %.m22 = sext i1 %i33 to i32
  %.n23 = xor i32 %.m22, -1
  %i37 = and i32 %i21, %.n23
  %i38 = or i32 %.sh20, %i20
  %i39 = add i32 %i38, %i37
  %.m24 = sext i1 %i17 to i32
  %.a25 = and i32 %i26, %.m24
  %.n26 = xor i1 %i17, true
  %.m27 = sext i1 %.n26 to i32
  %.a28 = and i32 %i39, %.m27
  %.o29 = or i32 %.a25, %.a28
  %.m30 = sext i1 %.n11 to i32
  %.a31 = and i32 %.o29, %.m30
  %i41 = zext i32 %.a31 to i64
  %.m32 = sext i1 %.n11 to i64
  %.a33 = and i64 %i41, %.m32
  %.o36 = or i64 %.a33, %.a35
  ret i64 %.o36
}

; Function Attrs: nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare i32 @llvm.abs.i32(i32, i1 immarg) #0

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
