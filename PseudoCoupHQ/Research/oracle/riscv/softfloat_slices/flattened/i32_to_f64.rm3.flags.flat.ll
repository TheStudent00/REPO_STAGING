; ModuleID = '<scratch>/fl/run/i32_to_f64.rm3.flags/i32_to_f64.rm3.flags.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local [2 x i64] @i32_to_f64_rm3_flags_flat(i32 noundef signext %arg) {
  %i = icmp eq i32 %arg, 0
  %.n7 = xor i1 %i, true
  %.m8 = sext i1 %.n7 to i64
  %.k1 = call i32 @llvm.abs.i32(i32 %arg, i1 false)
  %.k2 = call range(i32 0, 33) i32 @llvm.ctlz.i32(i32 %.k1, i1 true)
  %i3 = freeze i32 %.k2
  %i12 = zext i32 %.k1 to i64
  %i4 = add i32 %i3, 21
  %i8 = sub i32 1053, %i3
  %i9 = zext i32 %i8 to i64
  %.sh5 = shl i64 %i9, 52
  %i13 = zext i32 %i4 to i64
  %.sh6 = shl i64 %i12, %i13
  %i14 = freeze i64 %.sh6
  %.sh3 = lshr i32 %arg, 31
  %i6 = zext i32 %.sh3 to i64
  %.sh4 = shl i64 %i6, 63
  %i11 = or i64 %.sh5, %.sh4
  %i15 = add i64 %i11, %i14
  %.a9 = and i64 %i15, %.m8
  %i17 = insertvalue [2 x i64] [i64 0, i64 poison], i64 %.a9, 1
  ret [2 x i64] %i17
}

; Function Attrs: nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare i32 @llvm.abs.i32(i32, i1 immarg) #0

; Function Attrs: nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare i32 @llvm.ctlz.i32(i32, i1 immarg) #0

attributes #0 = { nocallback nofree nosync nounwind speculatable willreturn memory(none) }

!llvm.ident = !{!0, !0, !0, !0, !0}
!llvm.module.flags = !{!1, !2, !3, !5}

!0 = !{!"Ubuntu clang version 21.1.8 (6ubuntu1)"}
!1 = !{i32 1, !"wchar_size", i32 4}
!2 = !{i32 1, !"target-abi", !"lp64"}
!3 = distinct !{i32 6, !"riscv-isa", !4}
!4 = distinct !{!"rv64i2p1_m2p0_zmmul1p0"}
!5 = !{i32 8, !"SmallDataLimit", i32 0}
