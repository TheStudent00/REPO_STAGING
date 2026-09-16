; ModuleID = '<scratch>/fl/run/ui64_to_f64.rm4.value/ui64_to_f64.rm4.value.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local i64 @ui64_to_f64_rm4_value_flat(i64 noundef %arg) {
  %i = icmp eq i64 %arg, 0
  %.n23 = xor i1 %i, true
  %.m24 = sext i1 %.n23 to i64
  %i2 = icmp sgt i64 %arg, -1
  %.k1 = call range(i64 0, 65) i64 @llvm.ctlz.i64(i64 range(i64 1, -9223372036854775808) %arg, i1 true)
  %i11 = freeze i64 %.k1
  %i12 = trunc i64 %i11 to i8
  %i13 = add i8 %i12, -1
  %i20 = add i64 %i11, 4294967285
  %i21 = and i64 %i20, 4294967295
  %.sh5 = shl i64 %arg, %i21
  %i22 = freeze i64 %.sh5
  %i14 = zext i8 %i13 to i16
  %i15 = sub i16 1084, %i14
  %i24 = zext i8 %i13 to i64
  %.sh6 = shl i64 %arg, %i24
  %i25 = freeze i64 %.sh6
  %i26 = add i64 %i25, 512
  %i16 = icmp ult i64 %arg, 9007199254740992
  %.sh2 = lshr i64 %arg, 1
  %i5 = add i64 %.sh2, 512
  %.sh3 = lshr i64 %i5, 10
  %i9 = add i64 %.sh3, 4886405595696988160
  %i18 = zext i16 %i15 to i64
  %.sh4 = shl i64 %i18, 52
  %i19 = freeze i64 %.sh4
  %i23 = add i64 %i22, %i19
  %.sh7 = lshr i64 %i26, 10
  %i30 = icmp ult i64 %i26, 1024
  %.m9 = sext i1 %i30 to i64
  %.n10 = xor i64 %.m9, -1
  %i33 = and i64 %i19, %.n10
  %i34 = add i64 %.sh7, %i33
  %.n11 = xor i1 %i2, true
  %.m12 = sext i1 %.n11 to i64
  %.a13 = and i64 %i9, %.m12
  %.m15 = sext i1 %i16 to i64
  %.a16 = and i64 %i23, %.m15
  %.o17 = or i64 %.a13, %.a16
  %.n18 = xor i1 %i16, true
  %.c19 = and i1 %.n18, %i2
  %.m20 = sext i1 %.c19 to i64
  %.a21 = and i64 %i34, %.m20
  %.o22 = or i64 %.o17, %.a21
  %.a25 = and i64 %.o22, %.m24
  ret i64 %.a25
}

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
