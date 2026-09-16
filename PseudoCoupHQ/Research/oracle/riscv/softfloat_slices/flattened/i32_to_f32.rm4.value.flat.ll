; ModuleID = '<scratch>/fl/run/i32_to_f32.rm4.value/i32_to_f32.rm4.value.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local i64 @i32_to_f32_rm4_value_flat(i32 noundef signext %arg) {
  %i = and i32 %arg, 2147483647
  %i1 = icmp eq i32 %i, 0
  %i3 = icmp slt i32 %arg, 0
  %.m1 = sext i1 %i3 to i64
  %i4 = and i64 3472883712, %.m1
  %.k2 = call i32 @llvm.abs.i32(i32 %arg, i1 false)
  %i7 = icmp eq i32 %arg, 0
  %.k3 = call range(i32 0, 33) i32 @llvm.ctlz.i32(i32 range(i32 0, -2147483647) %.k2, i1 true)
  %i9 = freeze i32 %.k3
  %i10 = trunc i32 %i9 to i8
  %i11 = add i8 %i10, -1
  %.n4 = xor i1 %i7, true
  %.m5 = sext i1 %.n4 to i8
  %.a6 = and i8 %i11, %.m5
  %.m7 = sext i1 %i7 to i8
  %.a8 = and i8 31, %.m7
  %.o9 = or i8 %.a6, %.a8
  %.m14 = sext i1 %i7 to i32
  %.n15 = xor i32 %.m14, -1
  %.n10 = xor i1 %i1, true
  %.m32 = sext i1 %i1 to i64
  %.a33 = and i64 %i4, %.m32
  %.m11 = sext i1 %.n10 to i8
  %.a12 = and i8 %.o9, %.m11
  %i14 = sext i8 %.a12 to i32
  %i15 = sext i8 %.a12 to i16
  %i16 = sub i16 156, %i15
  %i17 = icmp sgt i8 %.a12, 6
  %i19 = zext i16 %i16 to i32
  %.sh13 = shl i32 %i19, 23
  %i21 = freeze i32 %.sh13
  %i22 = and i32 %i21, %.n15
  %i20 = and i32 %arg, -2147483648
  %i23 = add i32 %i14, -7
  %.sh16 = shl i32 %.k2, %i23
  %.sh17 = shl i32 %.k2, %i14
  %i24 = freeze i32 %.sh16
  %i25 = add i32 %i24, %i20
  %i26 = add i32 %i25, %i22
  %i27 = freeze i32 %.sh17
  %i28 = add i32 %i27, 64
  %.sh18 = lshr i32 %i28, 7
  %i32 = icmp ult i32 %i28, 128
  %.m20 = sext i1 %i32 to i32
  %.n21 = xor i32 %.m20, -1
  %i36 = and i32 %i21, %.n21
  %i37 = or i32 %.sh18, %i20
  %i38 = add i32 %i37, %i36
  %.m22 = sext i1 %i17 to i32
  %.a23 = and i32 %i26, %.m22
  %.n24 = xor i1 %i17, true
  %.m25 = sext i1 %.n24 to i32
  %.a26 = and i32 %i38, %.m25
  %.o27 = or i32 %.a23, %.a26
  %.m28 = sext i1 %.n10 to i32
  %.a29 = and i32 %.o27, %.m28
  %i40 = zext i32 %.a29 to i64
  %.m30 = sext i1 %.n10 to i64
  %.a31 = and i64 %i40, %.m30
  %.o34 = or i64 %.a31, %.a33
  ret i64 %.o34
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
