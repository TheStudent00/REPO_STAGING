; ModuleID = '<scratch>/fl/run/i64_to_f64.rm1.flags/i64_to_f64.rm1.flags.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local [2 x i64] @i64_to_f64_rm1_flags_flat(i64 noundef %arg) {
  %i = and i64 %arg, 9223372036854775807
  %i1 = icmp eq i64 %i, 0
  %i3 = icmp slt i64 %arg, 0
  %.m1 = sext i1 %i3 to i64
  %i4 = and i64 -4332462841530417152, %.m1
  %.k2 = call i64 @llvm.abs.i64(i64 %arg, i1 false)
  %i7 = icmp eq i64 %arg, 0
  %.k3 = call range(i64 0, 65) i64 @llvm.ctlz.i64(i64 range(i64 0, -9223372036854775807) %.k2, i1 true)
  %i9 = freeze i64 %.k3
  %i10 = trunc i64 %i9 to i8
  %i11 = add i8 %i10, -1
  %.n4 = xor i1 %i7, true
  %.m5 = sext i1 %.n4 to i8
  %.a6 = and i8 %i11, %.m5
  %.m7 = sext i1 %i7 to i8
  %.a8 = and i8 63, %.m7
  %.o9 = or i8 %.a6, %.a8
  %.m14 = sext i1 %i7 to i64
  %.n15 = xor i64 %.m14, -1
  %.n10 = xor i1 %i1, true
  %.m26 = sext i1 %i1 to i64
  %.a27 = and i64 %i4, %.m26
  %.m11 = sext i1 %.n10 to i8
  %.a12 = and i8 %.o9, %.m11
  %i14 = sext i8 %.a12 to i32
  %i15 = sext i8 %.a12 to i16
  %i16 = sub i16 1084, %i15
  %i17 = icmp sgt i8 %.a12, 9
  %i19 = zext i16 %i16 to i64
  %.sh13 = shl i64 %i19, 52
  %i21 = freeze i64 %.sh13
  %i22 = and i64 %i21, %.n15
  %i20 = and i64 %arg, -9223372036854775808
  %i23 = add i32 %i14, -10
  %i24 = zext i32 %i23 to i64
  %.sh16 = shl i64 %.k2, %i24
  %i25 = freeze i64 %.sh16
  %i26 = add i64 %i25, %i20
  %i27 = add i64 %i26, %i22
  %i28 = zext i32 %i14 to i64
  %.sh17 = shl i64 %.k2, %i28
  %i29 = freeze i64 %.sh17
  %.sh18 = lshr i64 %i29, 10
  %i31 = and i64 %i29, 1023
  %i32 = icmp ne i64 %i31, 0
  %i33 = icmp ult i64 %i29, 1024
  %.m20 = sext i1 %i33 to i64
  %.n21 = xor i64 %.m20, -1
  %i37 = and i64 %i21, %.n21
  %i40 = zext i1 %i32 to i64
  %i38 = or i64 %.sh18, %i20
  %i39 = add i64 %i38, %i37
  %.n22 = xor i1 %i17, true
  %.c23 = and i1 %.n10, %.n22
  %.c28 = and i1 %.n10, %i17
  %.m24 = sext i1 %.c23 to i64
  %.a25 = and i64 %i40, %.m24
  %.a32 = and i64 %i39, %.m24
  %.m29 = sext i1 %.c28 to i64
  %.a30 = and i64 %i27, %.m29
  %.o31 = or i64 %.a27, %.a30
  %.o33 = or i64 %.o31, %.a32
  %i42 = insertvalue [2 x i64] poison, i64 %.a25, 0
  %i43 = insertvalue [2 x i64] %i42, i64 %.o33, 1
  ret [2 x i64] %i43
}

; Function Attrs: nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare i64 @llvm.abs.i64(i64, i1 immarg) #0

; Function Attrs: nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare i64 @llvm.ctlz.i64(i64, i1 immarg) #0

attributes #0 = { nocallback nofree nosync nounwind speculatable willreturn memory(none) }

!llvm.ident = !{!0, !0, !0, !0, !0, !0, !0, !0, !0}
!llvm.module.flags = !{!1, !2, !3, !5}

!0 = !{!"Ubuntu clang version 21.1.8 (6ubuntu1)"}
!1 = !{i32 1, !"wchar_size", i32 4}
!2 = !{i32 1, !"target-abi", !"lp64"}
!3 = distinct !{i32 6, !"riscv-isa", !4}
!4 = distinct !{!"rv64i2p1_m2p0_zmmul1p0"}
!5 = !{i32 8, !"SmallDataLimit", i32 0}
