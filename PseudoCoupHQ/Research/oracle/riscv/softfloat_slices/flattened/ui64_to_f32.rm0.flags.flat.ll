; ModuleID = '<scratch>/fl/run/ui64_to_f32.rm0.flags/ui64_to_f32.rm0.flags.rv.flat.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

define dso_local i64 @ui64_to_f32_rm0_flags_flat(i64 noundef %arg) {
  %i = icmp eq i64 %arg, 0
  %.k1 = call range(i64 0, 65) i64 @llvm.ctlz.i64(i64 %arg, i1 true)
  %i2 = freeze i64 %.k1
  %i3 = trunc i64 %i2 to i8
  %i19 = sub i64 33, %i2
  %i20 = and i64 %i19, 255
  %i4 = add i8 %i3, -40
  %i5 = zext i8 %i4 to i32
  %i16 = add i8 %i3, -33
  %i6 = icmp ult i64 %arg, 16777216
  %i17 = icmp ugt i64 %arg, 2147483647
  %.n2 = xor i1 %i, true
  %.c3 = and i1 %i6, %.n2
  %.n22 = xor i1 %i6, true
  %.m4 = sext i1 %.c3 to i32
  %.a5 = and i32 %i5, %.m4
  %.m33 = sext i1 %i6 to i32
  %.m6 = sext i1 %i to i32
  %.a7 = and i32 24, %.m6
  %.o8 = or i32 %.a5, %.a7
  %.n12 = xor i32 %.m6, -1
  %i9 = trunc i64 %arg to i32
  %.sh9 = shl i32 %i9, %.o8
  %i10 = freeze i32 %.sh9
  %.sh10 = shl i32 %.o8, 23
  %i11 = freeze i32 %.sh10
  %i12 = sub i32 %i10, %i11
  %i13 = add i32 %i12, 1249902592
  %i14 = and i32 %i13, %.n12
  %.a34 = and i32 %i14, %.m33
  %.sh13 = lshr i64 %arg, %i20
  %i21 = freeze i64 %.sh13
  %.sh14 = shl i64 -1, %i20
  %i22 = freeze i64 %.sh14
  %i23 = xor i64 %i22, -1
  %i24 = and i64 %arg, %i23
  %i25 = icmp ne i64 %i24, 0
  %i26 = zext i1 %i25 to i64
  %i27 = or i64 %i21, %i26
  %i28 = trunc i64 %i27 to i32
  %i31 = zext i8 %i16 to i32
  %.sh15 = shl i32 %i9, %i31
  %i32 = freeze i32 %.sh15
  %i34 = sext i8 %i16 to i32
  %.sh27 = shl i32 %i34, 23
  %i45 = sub i32 1308622848, %.sh27
  %.m16 = sext i1 %i17 to i32
  %.a17 = and i32 %i28, %.m16
  %.n18 = xor i1 %i17, true
  %.m19 = sext i1 %.n18 to i32
  %.a20 = and i32 %i32, %.m19
  %.o21 = or i32 %.a17, %.a20
  %.m24 = sext i1 %.n22 to i32
  %.a25 = and i32 %.o21, %.m24
  %.m30 = sext i1 %.n22 to i64
  %i35 = add i32 %.a25, 64
  %.sh26 = lshr i32 %i35, 7
  %i36 = freeze i32 %.sh26
  %i37 = and i32 %.a25, 127
  %i38 = icmp ne i32 %i37, 0
  %i39 = icmp eq i32 %i37, 64
  %i40 = zext i1 %i39 to i32
  %i41 = xor i32 %i40, -1
  %i42 = and i32 %i36, %i41
  %i48 = zext i1 %i38 to i64
  %.a31 = and i64 %i48, %.m30
  %i43 = icmp eq i32 %i42, 0
  %.m28 = sext i1 %i43 to i32
  %.n29 = xor i32 %.m28, -1
  %i46 = and i32 %i45, %.n29
  %i47 = add i32 %i42, %i46
  %.a35 = and i32 %i47, %.m24
  %.o36 = or i32 %.a34, %.a35
  %i50 = zext i32 %.o36 to i64
  %i51 = shl i64 %i50, 32
  %i52 = or i64 %i51, %.a31
  ret i64 %i52
}

; Function Attrs: nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare i64 @llvm.ctlz.i64(i64, i1 immarg) #0

attributes #0 = { nocallback nofree nosync nounwind speculatable willreturn memory(none) }

!llvm.ident = !{!0, !0, !0, !0, !0, !0, !0, !0}
!llvm.module.flags = !{!1, !2, !3, !5}

!0 = !{!"Ubuntu clang version 21.1.8 (6ubuntu1)"}
!1 = !{i32 1, !"wchar_size", i32 4}
!2 = !{i32 1, !"target-abi", !"lp64"}
!3 = distinct !{i32 6, !"riscv-isa", !4}
!4 = distinct !{!"rv64i2p1_m2p0_zmmul1p0"}
!5 = !{i32 8, !"SmallDataLimit", i32 0}
