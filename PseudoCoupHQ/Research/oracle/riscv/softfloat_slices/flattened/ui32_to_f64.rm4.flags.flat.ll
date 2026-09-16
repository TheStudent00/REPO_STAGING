; ModuleID = '<scratch>/fl/run/ui32_to_f64.rm4.flags/ui32_to_f64.rm4.flags.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local [2 x i64] @ui32_to_f64_rm4_flags_flat(i32 noundef signext %arg) {
  %i = icmp eq i32 %arg, 0
  %.n4 = xor i1 %i, true
  %.m5 = sext i1 %.n4 to i64
  %.k1 = call range(i32 0, 33) i32 @llvm.ctlz.i32(i32 %arg, i1 true)
  %i2 = freeze i32 %.k1
  %i3 = add i32 %i2, 21
  %i4 = sub i32 1053, %i2
  %i5 = zext i32 %i4 to i64
  %.sh2 = shl i64 %i5, 52
  %i8 = zext i32 %i3 to i64
  %i7 = zext i32 %arg to i64
  %.sh3 = shl i64 %i7, %i8
  %i9 = freeze i64 %.sh3
  %i10 = add i64 %.sh2, %i9
  %.a6 = and i64 %i10, %.m5
  %i12 = insertvalue [2 x i64] [i64 0, i64 poison], i64 %.a6, 1
  ret [2 x i64] %i12
}

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
