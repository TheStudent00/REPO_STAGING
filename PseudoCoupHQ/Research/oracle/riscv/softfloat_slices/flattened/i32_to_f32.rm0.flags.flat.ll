; ModuleID = '<scratch>/fl/run/i32_to_f32.rm0.flags/i32_to_f32.rm0.flags.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local i64 @i32_to_f32_rm0_flags_flat(i32 noundef signext %arg) {
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
  %.m35 = sext i1 %i1 to i64
  %.a36 = and i64 %i4, %.m35
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
  %i30 = and i32 %i27, 127
  %i31 = icmp ne i32 %i30, 0
  %i32 = icmp eq i32 %i30, 64
  %i33 = zext i1 %i32 to i32
  %i34 = xor i32 %i33, -1
  %i35 = and i32 %.sh18, %i34
  %i43 = zext i1 %i31 to i64
  %i36 = icmp eq i32 %i35, 0
  %.m20 = sext i1 %i36 to i32
  %.n21 = xor i32 %.m20, -1
  %i40 = and i32 %i21, %.n21
  %i41 = or i32 %i35, %i20
  %i42 = add i32 %i41, %i40
  %.n22 = xor i1 %i17, true
  %.m26 = sext i1 %i17 to i32
  %.a27 = and i32 %i26, %.m26
  %.c23 = and i1 %.n10, %.n22
  %.m24 = sext i1 %.c23 to i64
  %.a25 = and i64 %i43, %.m24
  %.m28 = sext i1 %.n22 to i32
  %.a29 = and i32 %i42, %.m28
  %.o30 = or i32 %.a27, %.a29
  %.m31 = sext i1 %.n10 to i32
  %.a32 = and i32 %.o30, %.m31
  %i45 = zext i32 %.a32 to i64
  %.m33 = sext i1 %.n10 to i64
  %.a34 = and i64 %.a25, %.m33
  %.a37 = and i64 %i45, %.m33
  %.o38 = or i64 %.a36, %.a37
  %i47 = shl i64 %.o38, 32
  %i48 = or i64 %i47, %.a34
  ret i64 %i48
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
