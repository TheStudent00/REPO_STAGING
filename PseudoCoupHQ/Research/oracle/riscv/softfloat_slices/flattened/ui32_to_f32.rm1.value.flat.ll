; ModuleID = '<scratch>/fl/run/ui32_to_f32.rm1.value/ui32_to_f32.rm1.value.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local i64 @ui32_to_f32_rm1_value_flat(i32 noundef signext %arg) {
  %i = icmp eq i32 %arg, 0
  %.n23 = xor i1 %i, true
  %.m24 = sext i1 %.n23 to i32
  %i2 = icmp sgt i32 %arg, -1
  %.k1 = call range(i32 0, 33) i32 @llvm.ctlz.i32(i32 range(i32 1, -2147483648) %arg, i1 true)
  %i10 = freeze i32 %.k1
  %i11 = trunc i32 %i10 to i8
  %i12 = add i8 %i11, -1
  %i13 = zext i8 %i12 to i32
  %i14 = zext i8 %i12 to i16
  %i15 = sub i16 156, %i14
  %i16 = icmp ult i32 %arg, 16777216
  %.sh3 = lshr i32 %arg, 8
  %i8 = add i32 %.sh3, 1317011456
  %i18 = zext i16 %i15 to i32
  %.sh4 = shl i32 %i18, 23
  %i19 = freeze i32 %.sh4
  %i20 = add i32 %i13, -7
  %.sh5 = shl i32 %arg, %i20
  %i21 = freeze i32 %.sh5
  %i22 = add i32 %i21, %i19
  %.sh6 = shl i32 %arg, %i13
  %i23 = freeze i32 %.sh6
  %.sh7 = lshr i32 %i23, 7
  %i27 = icmp ult i32 %i23, 128
  %.m9 = sext i1 %i27 to i32
  %.n10 = xor i32 %.m9, -1
  %i30 = and i32 %i19, %.n10
  %i31 = add i32 %.sh7, %i30
  %.n11 = xor i1 %i2, true
  %.m12 = sext i1 %.n11 to i32
  %.a13 = and i32 %i8, %.m12
  %.m15 = sext i1 %i16 to i32
  %.a16 = and i32 %i22, %.m15
  %.o17 = or i32 %.a13, %.a16
  %.n18 = xor i1 %i16, true
  %.c19 = and i1 %.n18, %i2
  %.m20 = sext i1 %.c19 to i32
  %.a21 = and i32 %i31, %.m20
  %.o22 = or i32 %.o17, %.a21
  %.a25 = and i32 %.o22, %.m24
  %i32 = zext i32 %.a25 to i64
  ret i64 %i32
}

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
