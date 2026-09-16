; ModuleID = '<scratch>/fl/run/f16_to_f32.rm0.flags/f16_to_f32.rm0.flags.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local i64 @f16_to_f32_rm0_flags_flat(i64 %arg) {
  %i = trunc i64 %arg to i32
  %i1 = and i32 %i, 32768
  %i11 = and i32 %i, 512
  %i12 = icmp eq i32 %i11, 0
  %.m6 = sext i1 %i12 to i64
  %spec.select = and i64 16, %.m6
  %i2 = icmp eq i32 %i1, 0
  %.m7 = sext i1 %i2 to i32
  %i3 = lshr i64 %arg, 10
  %i4 = trunc i64 %i3 to i8
  %i5 = and i8 %i4, 31
  %i6 = trunc i64 %arg to i16
  %i7 = and i16 %i6, 1023
  %.q1 = icmp eq i8 %i5, 31
  %.q2 = icmp eq i8 %i5, 0
  %i16 = icmp eq i16 %i7, 0
  %.sh3 = shl i32 %i1, 16
  %i18 = freeze i32 %.sh3
  %i36 = or i32 %i18, 939524096
  %i20 = zext i16 %i7 to i32
  %.k4 = call range(i32 16, 33) i32 @llvm.ctlz.i32(i32 %i20, i1 true)
  %i21 = freeze i32 %.k4
  %i22 = add i32 %i21, 235
  %i23 = and i32 %i22, 255
  %.sh5 = shl i32 %i20, %i23
  %i24 = freeze i32 %.sh5
  %i25 = trunc i32 %i21 to i8
  %i26 = trunc i32 %i24 to i16
  %i27 = sub i8 21, %i25
  %.a8 = and i32 2139095040, %.m7
  %.n9 = xor i32 %.m7, -1
  %.a10 = and i32 -8388608, %.n9
  %i14 = or i32 %.a8, %.a10
  %.n11 = xor i1 %i16, true
  %.c12 = and i1 %.n11, %.q2
  %.c39 = and i1 %i16, %.q2
  %.c15 = or i1 %.q2, %.q1
  %.n16 = xor i1 %.c15, true
  %.m40 = sext i1 %.c39 to i32
  %.a41 = and i32 %i18, %.m40
  %.m13 = sext i1 %.c12 to i16
  %.a14 = and i16 %i26, %.m13
  %.m17 = sext i1 %.n16 to i16
  %.a18 = and i16 %i7, %.m17
  %.o19 = or i16 %.a14, %.a18
  %i34 = zext i16 %.o19 to i32
  %.sh27 = shl i32 %i34, 13
  %i35 = freeze i32 %.sh27
  %i37 = add i32 %i36, %i35
  %.m20 = sext i1 %.c12 to i8
  %.a21 = and i8 %i27, %.m20
  %.c32 = or i1 %.c12, %.n16
  %.m22 = sext i1 %.n16 to i8
  %.a23 = and i8 %i5, %.m22
  %.o24 = or i8 %.a21, %.a23
  %i32 = sext i8 %.o24 to i32
  %.sh26 = shl i32 %i32, 23
  %i33 = freeze i32 %.sh26
  %i38 = add i32 %i37, %i33
  %.m33 = sext i1 %.c32 to i32
  %.a34 = and i32 %i38, %.m33
  %.c29 = and i1 %.n11, %.q1
  %.c35 = and i1 %i16, %.q1
  %.m36 = sext i1 %.c35 to i32
  %.a37 = and i32 %i14, %.m36
  %.o38 = or i32 %.a34, %.a37
  %.o42 = or i32 %.o38, %.a41
  %.m30 = sext i1 %.c29 to i64
  %.a31 = and i64 %spec.select, %.m30
  %.m43 = sext i1 %.c29 to i32
  %.a44 = and i32 2143289344, %.m43
  %.o45 = or i32 %.o42, %.a44
  %i40 = zext i32 %.o45 to i64
  %.sh46 = shl i64 %i40, 32
  %i41 = freeze i64 %.sh46
  %i42 = or i64 %i41, %.a31
  ret i64 %i42
}

; Function Attrs: nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare i32 @llvm.ctlz.i32(i32, i1 immarg) #0

attributes #0 = { nocallback nofree nosync nounwind speculatable willreturn memory(none) }

!llvm.ident = !{!0, !0, !0, !0, !0, !0, !0}
!llvm.module.flags = !{!1, !2, !3, !5}

!0 = !{!"Ubuntu clang version 21.1.8 (6ubuntu1)"}
!1 = !{i32 1, !"wchar_size", i32 4}
!2 = !{i32 1, !"target-abi", !"lp64"}
!3 = distinct !{i32 6, !"riscv-isa", !4}
!4 = distinct !{!"rv64i2p1_m2p0_zmmul1p0"}
!5 = !{i32 8, !"SmallDataLimit", i32 0}
