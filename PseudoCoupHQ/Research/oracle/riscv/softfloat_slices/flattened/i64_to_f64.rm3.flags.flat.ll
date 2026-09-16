; ModuleID = '<scratch>/fl/run/i64_to_f64.rm3.flags/i64_to_f64.rm3.flags.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local [2 x i64] @i64_to_f64_rm3_flags_flat(i64 noundef %arg) {
  %i = icmp sgt i64 %arg, -1
  %i1 = and i64 %arg, 9223372036854775807
  %i2 = icmp eq i64 %i1, 0
  %.m1 = sext i1 %i to i64
  %.n2 = xor i64 %.m1, -1
  %i4 = and i64 -4332462841530417152, %.n2
  %i30 = and i64 1023, %.m1
  %.k3 = call i64 @llvm.abs.i64(i64 %arg, i1 false)
  %i7 = icmp eq i64 %arg, 0
  %.k4 = call range(i64 0, 65) i64 @llvm.ctlz.i64(i64 range(i64 0, -9223372036854775807) %.k3, i1 true)
  %i9 = freeze i64 %.k4
  %i10 = trunc i64 %i9 to i8
  %i11 = add i8 %i10, -1
  %.n5 = xor i1 %i7, true
  %.m6 = sext i1 %.n5 to i8
  %.a7 = and i8 %i11, %.m6
  %.m8 = sext i1 %i7 to i8
  %.a9 = and i8 63, %.m8
  %.o10 = or i8 %.a7, %.a9
  %.m15 = sext i1 %i7 to i64
  %.n16 = xor i64 %.m15, -1
  %.n11 = xor i1 %i2, true
  %.m28 = sext i1 %i2 to i64
  %.a29 = and i64 %i4, %.m28
  %.m12 = sext i1 %.n11 to i8
  %.a13 = and i8 %.o10, %.m12
  %i14 = sext i8 %.a13 to i32
  %i15 = sext i8 %.a13 to i16
  %i16 = sub i16 1084, %i15
  %i17 = icmp sgt i8 %.a13, 9
  %i19 = zext i16 %i16 to i64
  %.sh14 = shl i64 %i19, 52
  %i21 = freeze i64 %.sh14
  %i22 = and i64 %i21, %.n16
  %i20 = and i64 %arg, -9223372036854775808
  %i23 = add i32 %i14, -10
  %i24 = zext i32 %i23 to i64
  %.sh17 = shl i64 %.k3, %i24
  %i25 = freeze i64 %.sh17
  %i26 = add i64 %i25, %i20
  %i27 = add i64 %i26, %i22
  %i28 = zext i32 %i14 to i64
  %.sh18 = shl i64 %.k3, %i28
  %i29 = freeze i64 %.sh18
  %i31 = add i64 %i29, %i30
  %i33 = and i64 %i29, 1023
  %i34 = icmp ne i64 %i33, 0
  %i42 = zext i1 %i34 to i64
  %.sh20 = lshr i64 %i31, 10
  %i35 = icmp ult i64 %i31, 1024
  %.m22 = sext i1 %i35 to i64
  %.n23 = xor i64 %.m22, -1
  %i39 = and i64 %i21, %.n23
  %i40 = or i64 %.sh20, %i20
  %i41 = add i64 %i40, %i39
  %.n24 = xor i1 %i17, true
  %.c25 = and i1 %.n24, %.n11
  %.c30 = and i1 %i17, %.n11
  %.m26 = sext i1 %.c25 to i64
  %.a27 = and i64 %i42, %.m26
  %.a34 = and i64 %i41, %.m26
  %.m31 = sext i1 %.c30 to i64
  %.a32 = and i64 %i27, %.m31
  %.o33 = or i64 %.a29, %.a32
  %.o35 = or i64 %.o33, %.a34
  %i44 = insertvalue [2 x i64] poison, i64 %.a27, 0
  %i45 = insertvalue [2 x i64] %i44, i64 %.o35, 1
  ret [2 x i64] %i45
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
